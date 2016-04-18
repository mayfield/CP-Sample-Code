
import logging
import gc

HISTORICAL_filename = None
HISTORICAL_log = []
HISTORICAL_next_index = 0


# Obtain a response
def map_request_to_response(request):
    """

    :param request:
    :type request: dict
    :return:
    """
    response = None
    if request['code'] in (0x21, 0x22):
        # is a 'update_network_state' or 'register_wireless_device'
        response = b'\xC5\x0C\x00\x23\xC8\x00\x00\x00\x05\x00\x15\x44\x01\x30\xE8'

    elif request['code'] == 0x24:
        response = get_next_data_log()

    else:
        raise ValueError("Bad Command:{}".format(request))

    return response


def get_next_data_log():
    """

    :return:
    :rtype: bytes
    """
    global HISTORICAL_filename, HISTORICAL_log, HISTORICAL_next_index

    HISTORICAL_next_index += 1
    if HISTORICAL_next_index >= len(HISTORICAL_log):
        if False:
            # then ROLL the log & restart
            HISTORICAL_next_index = 0
        else:  # signal end-of-queue
            return b'\xC5\x07\x00\x24\xC8\x00\x00\x00\x0C\x3D'

    return HISTORICAL_log[HISTORICAL_next_index]


def load_data_log(filename):
    """

    :param filename:
    :return:
    :rtype: bytes
    """
    global HISTORICAL_filename, HISTORICAL_log, HISTORICAL_next_index

    # then load new data
    logging.info("Process NEW file:{}".format(filename))
    HISTORICAL_filename = filename

    HISTORICAL_log = []
    HISTORICAL_next_index = -1

    source = open(filename, 'r')

    for line in source:
        # we assume us like "   (0, b'\xC5\x07\x00\x21\x01', b'\xC5\x0C\x00\x23\xC8'),"
        if len(line) < 2:
            continue

        data = line.split(',')
        # should be like:
        # DEBUG:root:[    (0]
        # DEBUG:root:[ b'\xC5\x07\x00\x21\x01\x80\xED\x53\x0B\xF4']
        # DEBUG:root:[ b'\xC5\x0C\x00\x23\xC8\x00\x00\x00\x05\x00\x15\x44\x01\x30\xE8')]
        # DEBUG:root:[
        # ]

        # we only want to keep the code 56 messages
        if len(data[2]) > 20 and data[2][17:19] == '56':
            logging.debug("GOOD:{}".format(data[2]))
            data = data[2]
            if data[-1] == ')':
                data = data[:-1]
            data = eval(data)
            HISTORICAL_log.append(data)
        else:
            logging.debug("TOSS:{}".format(data[2]))

    source.close()
    del source

    gc.collect()

    return

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    logging.info("Hello - here we go!")

    load_data_log('01_messages.txt')
