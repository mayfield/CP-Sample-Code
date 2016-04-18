
import struct
# from common.format_bytes import format_bytes
from monnit.utility import parse_monnit_utc_le32, get_monnit_utc_le32, \
    format_timestamp, convert_byte_sint
from monnit.sensor_data import MonnitSensorData

MINIMUM_LENGTH = 5
START_DELIMITER = 0xC5

OFFSET_START = 0
OFFSET_LENGTH = 1
OFFSET_OPTIONS = 2
OFFSET_COMMAND = 3
OFFSET_PAYLOAD = 4
OFFSET_CRC = -1


class MonnitProtocolError(ValueError):
    """
    Error relates to basic format - so bad command, CRC, etc
    """
    pass


class MonnitProtocolDataError(ValueError):
    """
    Error relates to sensor data - so basic message was okay, but sensor data bad
    """
    pass


def form_isvalid(message):
    """
    Given the message, return expected_length if okay, else throw exception

    It confirms:
    - is not None/null and at least 'minimum length'
    - that start delimiter is okay
    - assuming <len> byte is valid, that message is expected length (with or without CRC added)

    :param message:
    :type message: bytes
    :return:
    :rtype: int
    """
    if message is None or len(message) < MINIMUM_LENGTH:
        raise ValueError("message too short")

    if message[0] != START_DELIMITER:
        raise ValueError("message lacks START delimiter")

    expect_length = message[1] + 2

    # the message ought to be == expect_length, or +1 if CRC is already appended
    if len(message) != expect_length and len(message) != expect_length + 1:
        raise ValueError("message len=%d, expect %d or %d" % (len(message), expect_length,
                                                              expect_length + 1))

    return expect_length


class MonnitProtocol(object):

    COMMAND_NAME = {
        'form_network': {'cmd': 0x20, 'len': 5},
        'update_network_state': {'cmd': 0x21, 'len': 5},
        'register_wireless_device': {'cmd': 0x22, 'len': 4},
        'network_status_rsp': {'cmd': 0x23, 'len': 10},
        'queued_message_rsp': {'cmd': 0x24, 'len': 5},
        'parent_message': {'cmd': 0x52, 'len': 12},
        'data_log_message': {'cmd': 0x56, 'len': None},
    }

    COMMAND_CODE = {
        0x20: 'form_network',
        0x21: 'update_network_state',
        0x22: 'register_wireless_device',
        0x23: 'network_status_rsp',
        0x24: 'queued_message_rsp',
        0x52: 'parent_message',
        0x56: 'data_log_message',
    }

    NETWORK_STATE_RESET_IDLE = 0
    NETWORK_STATE_ACTIVE_RESUME = 1
    NETWORK_STATE_ENUM = (0, 1)
    NETWORK_STATE_NAME = ('reset/idle', 'active/resume')

    PROTOCOL_MIN = 0
    PROTOCOL_MAX = 3

    # the state machine nodes for server
    STATE_UNKNOWN = 'unknown'
    STATE_RESET = 'reset'
    STATE_RESUME = 'resume'
    STATE_REGISTER = 'register'
    STATE_POLL = 'poll'

    def __init__(self):

        self.version = 1

        # add the callbacks - avoids circular def issues
        self.COMMAND_NAME['update_network_state']['fnc'] = self._parse_x21_update_network_state
        self.COMMAND_NAME['register_wireless_device']['fnc'] = self._parse_x22_register_device
        self.COMMAND_NAME['network_status_rsp']['fnc'] = self._parse_x23_network_status
        self.COMMAND_NAME['queued_message_rsp']['fnc'] = self._parse_x24_queued
        self.COMMAND_NAME['parent_message']['fnc'] = self._parse_x52_parent
        self.COMMAND_NAME['data_log_message']['fnc'] = self._parse_x56_data_log

        self.state = self.STATE_UNKNOWN
        self.sensor_list = []

        self._index = -1
        self._gateway_address = 0
        self._gateway_bytes = b'\x00'

        # generic sensor processor
        self.sensor = MonnitSensorData()

        return

    def reset_state_machine(self):
        """

        :return:
        :rtype: int
        """
        self.state = self.STATE_UNKNOWN
        self._index = -1
        return

    def get_gateway_address(self):
        """

        :return:
        :rtype: int
        """
        return self._gateway_address

    def set_gateway_address(self, address):
        """

        :param address:
        :type address: int
        :return:
        """
        self._gateway_address = 0
        self._gateway_bytes = struct.pack("<I", address)
        return

    def add_sensor_id(self, address):
        """

        :param address:
        :type address: int
        :return:
        """
        if address not in self.sensor_list:
            self.sensor_list.append(address)
        self._index = -1

        return

    def clear_sensor_list(self):
        """

        :return:
        """
        self.sensor_list = []
        self._index = -1
        return

    def remove_sensor_id(self, address):
        """

        :param address:
        :type address: int
        :return:
        """
        if address in self.sensor_list:
            self.sensor_list.remove(address)
        self._index = -1

        return

    def next_request(self):
        """
        Based on 'state', obtain the next request to send to gateway

        :return: the next request, or None to delay
        :rtype: bytes
        """
        if self.state == self.STATE_UNKNOWN:
            # send the Update network State reset/idle
            result = self._format_x21_update_network_state(b'\x00')
            self.state = self.STATE_RESET

        elif self.state == self.STATE_RESET:
            # send the Update network State active/resume
            result = self._format_x21_update_network_state(b'\x01')
            self.state = self.STATE_RESUME

        elif self.state == self.STATE_RESUME:
            # start sending the wireless sensor id's
            if len(self.sensor_list):
                self._index = 0
                result = self._format_x22_register_device(self.sensor_list[self._index])
                self.state = self.STATE_REGISTER
            else:  # delay to start the poll, as there are NO registered addresses
                result = None
                self._index = -1
                self.state = self.STATE_POLL

        elif self.state == self.STATE_REGISTER:
            # start sending the wireless sensor id's
            self._index += 1
            if len(self.sensor_list) > self._index:
                result = self._format_x22_register_device(self.sensor_list[self._index])
                # self.state = self.STATE_REGISTER

            else:  # last address has been sent, so do one last update state
                # not sure why, but the Monnit server tool does this.
                result = self._format_x21_update_network_state(b'\x01')
                self.state = self.STATE_POLL
                self._index = -1

        elif self.state == self.STATE_POLL:
            # the next poll, self._index is managed internally
            result = self._format_x24_queued_message_req()

        else:
            raise ValueError("Bad state")

        return result

    def parse_message(self, message):
        """
        Given a binary message, return python keyed dict of value

        TODO: support concatenated messages? How to handle trailing partial?

        :param message: the raw source from media
        :type message: bytes
        :return: a LIST of messages parsed from source
        """
        from monnit.crc import crc_isvalid

        # Confirm there is some data, but discard lead until START_DELIMITER is seen
        if message is None or len(message) < MINIMUM_LENGTH:
            raise ValueError("message too short")

        while message[0] != START_DELIMITER:
            # drop leading byte until is 0xC5
            message = message[1:]

        # this throws ValueError is CRC or form is not correct
        crc_isvalid(message)

        # save the original message
        result = dict()
        result['raw'] = message

        # break out the command byte
        x = message[OFFSET_COMMAND]
        if x not in self.COMMAND_CODE:
            # was not in the keyed list of CODES
            raise ValueError("message unknown command=%02X" % x)

        result['code'] = x
        # use the CODE to lookup the name
        result['cmd'] = self.COMMAND_CODE[result['code']]
        # use the NAME to lookup the info data
        info = self.COMMAND_NAME[result['cmd']]

        payload = message[OFFSET_PAYLOAD:OFFSET_CRC]

        if info['len'] is not None and len(payload) != info['len']:
            raise ValueError("message payload is incorrect. len=%d expect=%d" % (len(payload),
                                                                                 info['len']))
        # else if 'len' is none, then no easy answer for length - allow the ['fnc'] to validate

        try:
            assert callable(info['fnc'])
            result = info['fnc'](result, payload)
        except KeyError:
            raise KeyError("Known command (%s), has no handling routine." % result['cmd'])

        # print(format_bytes('raw', message))
        # print(format_bytes('pay', payload))

        return result

    def _format_x21_update_network_state(self, state, monnit_time=None):
        """
        Code: 0x21

        :param state: the desired state in (0, 1)
        :type state: bytes
        :param monnit_time: the desired state in (0, 1)
        :type monnit_time: bytes
        :return:
        :rtype: bytes
        """
        if state not in (b'\x00', b'\x01'):
            raise MonnitProtocolError("x21 bad state")

        if monnit_time is None:
            monnit_time = get_monnit_utc_le32()

        # build the payload
        # b'\x21\x01\x39\xB5\x31\x0B'
        result = b'\x21' + state + monnit_time

        # b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E'
        return self.wrap_payload(result)

    def _parse_x21_update_network_state(self, result, payload):
        """
        Code: 0x21

        :param result: the building parsed result
        :type result: dict
        :param payload: message payload
        :type payload: bytes
        :return:
        :rtype: dict
        """
        # example: 01 39 B5 31 0B
        #
        result['state'] = self.__parse_state_byte(payload[0])

        x = struct.unpack("<I", payload[1:])[0]
        # if self.version == 1:
        #     # then is seconds since Monnit Epoch of 2010-01-01
        # else:  # is 1/2 seconds since
        result['time'] = x

        return result

    def _format_x22_register_device(self, address):
        """
        Code: 0x22

        :param address: the device ID per label, such as 95412
        :type address: int
        :return:
        :rtype: bytes
        """
        result = b'\x22' + struct.pack("<I", address)
        return self.wrap_payload(result)

    @staticmethod
    def _parse_x22_register_device(result, payload):
        """
        Code: 0x22

        :param result: the building parsed result
        :type result: dict
        :param payload: message payload
        :type payload: bytes
        :return:
        :rtype: dict
        """
        result['address'] = struct.unpack("<I", payload)[0]
        return result

    def _parse_x23_network_status(self, result, payload):
        """
        Code: 0x23

        :param result: the building parsed result
        :type result: dict
        :param payload: message payload
        :type payload: bytes
        :return:
        :rtype: dict
        """
        # example: \xC8\x00\x00\x00\x02\x00\x07\x80\x01\x30,
        #          APN             ,cnt,
        #

        # APN number, 4-byte LE
        x = struct.unpack("<I", payload[0:4])[0]
        result['apn_id'] = x

        # device count, 2-byte LE
        x = struct.unpack("<H", payload[4:6])[0]
        result['dev_count'] = x

        # channel, 1-byte
        result['channel'] = payload[6]

        # network id, 1-byte
        result['network'] = payload[7]

        # state, 1-byte
        result['state'] = self.__parse_state_byte(payload[8])

        x = self.__parse_protocol_status_byte(payload[9])
        if x != 0:
            # ignore if okay (aka: we assume is okay)
            result['state'] = self.__parse_protocol_status_byte(payload[7])

        return result

    def reset_poll_counter(self, counter=None):
        if counter is None:
            # since we 'pre-increment', we start -1 to make 0
            self._index = -1
        else:
            self._index = int(counter - 1)
        return

    def _format_x24_queued_message_req(self, counter=None):
        """
        Code: 0x24

        :param counter: allow forcing a counter value (over-writes self._index)
        :type counter: int
        :return:
        :rtype: bytes
        """
        if counter is None:
            self._index += 1
        else:
            self._index = int(counter)

        if self._index > 255 or self._index < 0:
            # force to be 0-255
            self._index = 0

        # build the payload
        result = b'\x24' + self._gateway_bytes + bytes([self._index])
        return self.wrap_payload(result)

    @staticmethod
    def _parse_x24_queued(result, payload):
        """
        Code: 0x24

        :param result: the payload to parse
        :type result: dict
        :param payload: message payload
        :type payload: bytes
        :return: the result with the payload parsed
        :rtype: dict
        """
        # example: \x85\x03\x00\x00\x00
        #          \xC8\x00\x00\x00\x0C
        #

        # Device Id, 4-byte LE
        x = struct.unpack("<I", payload[0:4])[0]
        result['dev_id'] = x

        # queued message status, 1-byte
        result['status'] = payload[4]

        return result

    @staticmethod
    def _parse_x52_parent(result, payload):
        """
        Code: 0x52

        :param result: the payload to parse
        :type result: dict
        :param payload: message payload
        :type payload: bytes
        :return: the result with the payload parsed
        :rtype: dict
        """
        # example: \x85\x03\x00\x00\x00
        #          \xC8\x00\x00\x00\x0C
        #

        # Device Id, 4-byte LE
        x = struct.unpack("<I", payload[0:4])[0]
        result['dev_id'] = x

        # Parent Id, 4-byte LE
        x = struct.unpack("<I", payload[4:8])[0]
        result['parent'] = x

        # version, X.X.X.X
        x = "%d.%d.%d.%d" % (payload[8], payload[9], payload[10], payload[11])
        result['version'] = x

        return result

    def _parse_x56_data_log(self, result, payload):
        """
        Code: 0x56

        :param result: the payload to parse
        :type result: dict
        :param payload: message payload
        :type payload: bytes
        :return: the result with the payload parsed
        :rtype: dict
        """
        # example: \x85\x03\x00\x00\x00
        #          \xC8\x00\x00\x00\x0C
        #

        # Device Id, 4-byte LE
        result['dev_id'] = struct.unpack("<I", payload[0:4])[0]

        # Sample Time, 4-byte LE
        x = parse_monnit_utc_le32(payload[4:8])
        if x == 1262329200.0:
            # then time is zero!
            result['time'] = 0
        else:
            result['time'] = x
            result['time_str'] = format_timestamp(x)

        # RSSI, 1-byte s8
        result['ap_rssi'] = convert_byte_sint(payload[8])
        result['dev_rssi'] = convert_byte_sint(payload[9])

        # Voltage 1-byte per PDF
        result['battery'] = (150 + payload[10]) / 100.0

        result = self.sensor.parse_any(result, payload[11:])

        # # Sensor Type, 2-byte LE
        # result['sensor_type'] = struct.unpack("<H", payload[11:13])[0]
        #
        # # Sensor State, 1-byte
        # result['sensor_state'] = payload[13]
        #
        # # Sensor Data, ?-byte
        # if len(payload) > 14:
        #     result['sensor_data'] = payload[14:]
        # else:
        #     result['sensor_data'] = None

        return result

    def __parse_state_byte(self, data):
        """

        :param data:
        :type data: int
        :return:
        :rtype: str
        """
        # state, 1-byte
        if data not in self.NETWORK_STATE_ENUM:
            raise ValueError("NetworkState: bad state value:%s" % data)

        return self.NETWORK_STATE_NAME[data]

    def __parse_protocol_status_byte(self, data):
        """

        :param data:
        :type data: int
        :return:
        :rtype: str
        """
        # handle the upper nibble - the protocol
        x = (data & 0xF0) >> 4
        if x > self.PROTOCOL_MAX:
            raise ValueError("Protocol Version outside 0-3 range:%s" % x)

        self.version = int(x)

        # if data not in self.NETWORK_STATE_ENUM:
        #     raise ValueError("NetworkState: bad state value:%s" % x)

        return data & 0x0F

    @staticmethod
    def wrap_payload(payload):
        """
        Given the core of a message, add the header, len, and CRC

        So convert:      b'\x21\x01\x39\xB5\x31\x0B'
        into b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E'

        :param payload:
        :type payload: bytes
        :return:
        """
        from monnit.crc import crc_append

        result = b'\xC5' + bytes([len(payload) + 1]) + b'\x00' + payload
        return crc_append(result)
