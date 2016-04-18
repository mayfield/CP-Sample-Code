
import logging
import os
import serial
import time

import monnit.protocol as protocol
from common.format_bytes import format_bytes
from monnit.imonnit import ImonnitUpload


imonnit_uploader = None


def bytes_to_constant(data: bytes):
    """
    Given a binary 'bytes' string, convert to a Python parsable string.
    Example: 0xC5 0x07 0x00 0x21 becomes "b'\xc5\x07\x00\x21'"

    :param data: the raw bytes input
    :return: the processed string response
    :rtype: str
    """
    result = "b\'"
    for ch in data:
        result += "\\x%02X" % ch
    result += "\'"
    return result


def file_save_timestamp(filename):
    """
    Given a simple filename such as 'dump.txt', if it exists, rename to include the timestamp
    This frees up the original filename 'space' without losing the original. So the file
    'dump.txt' would become 'dump_20160110_082834.txt'

    :param filename: the file to save
    :return:
    """
    import os.path

    base_name = None

    if os.path.exists(filename):
        if not os.path.isfile(filename):
            raise ValueError("Can only work on regular file")

        # split 'docs/dump.txt' to 'docs' and 'dump.txt'
        path_name, base_name = os.path.split(filename)

        # see about an extension?
        x = base_name.rfind('.')
        if x > 0:
            # then we have an extension, split 'dump.txt' to be 'dump' and 'txt'
            ext_name = base_name[x+1:]
            base_name = base_name[:x]
        else:
            ext_name = None

        # add the time-stamp, and optionally re-attach the extension
        base_name += time.strftime("_%Y%m%d_%H%M%S")
        if ext_name is not None:
            base_name += '.' + ext_name

        # logging.debug("final:[{}]".format(base_name))
        if len(path_name):
            base_name = os.path.join(path_name, base_name)

    else:
        logging.debug("filename:{} doesn't exist".format(filename))

    return base_name

# x = file_save_timestamp('messages.txt')
# logging.debug("final:[{}]".format(x))
# logging.debug("")
#
# x = file_save_timestamp('monnit/docs/01 in.txt')
# logging.debug("final:[{}]".format(x))
# logging.debug("")


def move_old_file(filename):
    # save any older files
    _name = file_save_timestamp(filename)
    if _name is not None:
        # then move the old file
        os.rename(filename, _name)
    return


def main_usb_drain(loop=False, process=False):
    """
    Read the actual USB and save the data.

    :param loop: T to keep running after END-OF-QUEUE, F causes run() to stop
    :type loop: bool
    :param process: T to process the data & send alerts, F just create files
    :type process: bool
    :return:
    """

    # def serial_read(ser_han):
    #     data = ''
    #     start = time.time()

    from monnit.site_config import SERIAL_PORT_NAME, SERIAL_PORT_ID, GWAY_ADDRESS, \
        SENSOR_ADDRESS_LIST, MESSAGE_FILENAME, IMONNIT_HOSTNAME, POLL_CYCLE_SECS
    from monnit.sensor_demo import SensorDemo
    global imonnit_uploader

    if IMONNIT_HOSTNAME is not None:
        # then we enable uploading
        imonnit_uploader = ImonnitUpload()
        imonnit_uploader.set_apn_id(200)
    else:  # disable, set to None
        imonnit_uploader = None

    if MESSAGE_FILENAME is None:
        dump_file = None
    else:
        # save any older files
        _name = file_save_timestamp(MESSAGE_FILENAME)
        if _name is not None:
            # then move the old file
            os.rename(MESSAGE_FILENAME, _name)

        dump_file = open(MESSAGE_FILENAME, 'w')

    logging.info("Opening Gateway on port:{}".format(SERIAL_PORT_NAME))
    ser = serial.Serial(
            port=SERIAL_PORT_ID,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            timeout=1.0
    )

    gway = protocol.MonnitProtocol()
    gway.set_gateway_address(GWAY_ADDRESS)
    _my_sensors = dict()
    for address in SENSOR_ADDRESS_LIST:
        gway.add_sensor_id(address)
        sensor = SensorDemo(address)
        _my_sensors[address] = sensor

    # make sure we start at beginning of everything
    gway.reset_state_machine()

    # skip the first state - maybe it flushes the data?
    # obj.state = obj.STATE_RESET

    index = 0
    while True:
        request = gway.next_request()
        logging.debug("%03d: %s" % (index, format_bytes("REQ", request)))
        ser.write(request)

        # allow response to queue up - reduce IO blocking cost
        time.sleep(0.10)
        start_time = time.time()

        # assume the serial timeout will return for us
        retry = 0
        response = b'\x00'
        while retry < 3:
            response = ser.read(256)
            if len(response) == 0:
                retry += 1
                logging.debug("     retry:%d" % retry)
            else:
                break

        logging.debug("     %s" % format_bytes("RSP", response))

        if dump_file is not None:
            message = "    (%d, " % index + bytes_to_constant(request) + ", " + \
                      bytes_to_constant(response) + "),"
            dump_file.write(message + '\n')

        if len(response) > 0:
            parsed = gway.parse_message(response)
            # logging.debug("     {}".format(parsed))

            if process:
                # then process the message
                if parsed['code'] == 0x56:
                    # handle the data
                    sensor = _my_sensors[parsed['dev_id']]
                    assert isinstance(sensor, SensorDemo)
                    sensor.process_data(parsed)

                    if imonnit_uploader is not None:
                        # queue the raw binary
                        imonnit_uploader.queue_message(response)

            # we'll exit when we hit the final queued message
            if parsed['code'] == 0x24 and parsed['status'] == 12:
                # then end of queue seen

                if not loop:
                    # then break & stop
                    logging.info("End of Queue Seen, stopping")
                    break
                else:  # else, make sure the counter remains zero
                    gway.reset_poll_counter()

        index += 1

        now = time.time()

        # handle the iMonnit Upload (is not ideal place! Okay for demo)
        if imonnit_uploader is not None:
            assert isinstance(imonnit_uploader, ImonnitUpload)
            imonnit_uploader.do_upload_or_heartbeat(now)

        # delay to 'finish out' our cycle
        diff = now - start_time
        if diff < POLL_CYCLE_SECS:
            time.sleep(POLL_CYCLE_SECS - diff)

    if dump_file is not None:
        dump_file.close()
    ser.close()
    return


def main_file(filename):
    """
    Open a historical file, and use it to drive the state machine

    :param filename: the log file to open
    :type filename: str
    :return:
    """
    import monnit.historical_data as historical
    from monnit.sensor_demo import SensorDemo
    from monnit.site_config import GWAY_ADDRESS, SENSOR_ADDRESS_LIST, MESSAGE_FILENAME, \
        IMONNIT_HOSTNAME
    global imonnit_uploader

    if IMONNIT_HOSTNAME is not None:
        imonnit_uploader = ImonnitUpload
    else:
        imonnit_uploader = None

    if MESSAGE_FILENAME is None:
        dump_file = None
    else:
        # save any older files
        move_old_file(MESSAGE_FILENAME)
        dump_file = open(MESSAGE_FILENAME, 'w')

    gway = protocol.MonnitProtocol()
    gway.set_gateway_address(GWAY_ADDRESS)
    _my_sensors = dict()
    for address in SENSOR_ADDRESS_LIST:
        gway.add_sensor_id(address)
        sensor = SensorDemo(address)
        _my_sensors[address] = sensor

    # make sure we start at beginning of everything
    gway.reset_state_machine()

    # skip the first state - maybe it flushes the data?
    # obj.state = obj.STATE_RESET

    historical.load_data_log(filename)

    index = 0
    while True:
        request = gway.next_request()
        # logging.debug("%03d: %s" % (index, format_bytes("REQ", request)))

        # for this, we first parse-out the request
        parsed = gway.parse_message(request)
        response = historical.map_request_to_response(parsed)
        logging.debug("     %s" % format_bytes("RSP", response))

        if dump_file is not None:
            message = "    (%d, " % index + bytes_to_constant(request) + ", " + \
                      bytes_to_constant(response) + "),"
            dump_file.write(message + '\n')

        if len(response) > 0:
            parsed = gway.parse_message(response)

            if parsed['code'] == 0x56:
                # handle the data
                sensor = _my_sensors[parsed['dev_id']]
                assert isinstance(sensor, SensorDemo)
                sensor.process_data(parsed)

            # logging.debug("     {}".format(parsed))

            if True:
                # we'll exit when we hit the final queued message
                if parsed['code'] == 0x24 and parsed['status'] == 12:
                    # then end of queue seen
                    logging.info("End of Queue Seen, stopping")
                    break

        index += 1

    for address in SENSOR_ADDRESS_LIST:
        sensor = _my_sensors[address]
        assert isinstance(sensor, SensorDemo)
        logging.info(sensor.report())

    if dump_file is not None:
        dump_file.close()
    return


def initialize_logger():
    """
    Init my logger to both send to display & file

    :return:
    """
    from monnit.site_config import LOGGING_FILENAME

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    if LOGGING_FILENAME is not None:
        # save any older files
        move_old_file(LOGGING_FILENAME)
        handler = logging.FileHandler(LOGGING_FILENAME,"w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return

if __name__ == '__main__':

    initialize_logger()

    mode = 2

    if mode == 0:
        logging.info("Loading data from history")
        main_file('04_messages.txt')

    elif mode == 1:
        logging.info("Reading USB until empty, but do not act")
        main_usb_drain(loop=False, process=False)

    elif mode == 2:
        logging.info("Reading USB as loop, processing")
        main_usb_drain(loop=True, process=True)
    else:
        raise ValueError("run() - unknown mode!")
