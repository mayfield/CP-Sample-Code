__author__ = 'Lynn'

# import json
import copy

import serial

from data.cp_api import ApiRouterDisk


class SerialSettings(object):

    PORT_LIMIT = 20

    def __init__(self):

        self.logger = None

        self.api = ApiRouterDisk()

        # note that instance are zero-based, for if max_port = 2, then valid instance in (0, 1)
        self._max_ports = self.get_value("max_ports", serial_instance=None)
        assert isinstance(self._max_ports, int)
        assert 0 <= self._max_ports <= self.PORT_LIMIT

        return

    @staticmethod
    def validate_setting_name(setting):
        """
        test a setting name

        :param setting: the setting name, such as "ip_port" or "idle_timeout"
        :type setting: str
        :return: setting value, or throws exception
        :rtype: str
        """
        if not isinstance(setting, str):
            raise TypeError("setting name must be Type string")

        setting = setting.lower().strip()
        if setting not in SETTINGS_MAP:
            raise ValueError("Unknown setting name: {0}".format(setting))

        return setting

    def validate_serial_instance(self, serial_instance):
        """
        test a serial port instance (0-based) - not related to actual serial port numbers

        :param serial_instance: the setting name, such as "ip_port" or "idle_timeout"
        :type serial_instance: str, int, or None
        :return: serial instance value, or throws exception
        :rtype: int
        """
        if serial_instance is not None:
            if isinstance(serial_instance, str):
                serial_instance = int(serial_instance.strip())

            if not (0 <= serial_instance < self._max_ports):
                if 1 == self._max_ports:
                    # we only support 1 index, which is 0
                    raise ValueError("Serial Instance must be 0(zero)")
                else:
                    raise ValueError("Serial Instance must be between 0(zero) and {0}".format(self._max_ports))

        return serial_instance

    def get_value(self, setting, serial_instance):
        """

        :param setting: the setting name, such as "ip_port" or "idle_timeout"
        :type setting: str
        :param serial_instance: the zero-based index
        :type serial_instance: str, int, or None
        :return:
        """
        setting = self.validate_setting_name(setting)
        serial_instance = self.validate_serial_instance(serial_instance)

        maps = SETTINGS_MAP[setting]
        assert isinstance(maps, dict)
        if serial_instance is None:
            # then is a group value, so no instance (like "/config/serial/max_port")
            api_path = copy.copy(maps["path"])
        else:  # else with instance (like "/config/serial/0/baud")
            api_path = maps["path"] % serial_instance
        assert isinstance(api_path, str)

        value = self.api.get(api_path)

        if self.logger is not None:
            self.logger.debug("Setting.get({0}) = {1}".format(api_path, value))

        if value is None and "default" in maps:
            # handle the default case - not existing (should also put?)
            value = maps["default"]

        return value

    def put_value(self, setting, serial_instance, value):
        """

        :param setting: the setting name, such as "ip_port" or "idle_timeout"
        :type setting: str
        :param serial_instance: the zero-based index
        :type serial_instance: str, int, or None
        :return:
        """
        setting = self.validate_setting_name(setting)
        serial_instance = self.validate_serial_instance(serial_instance)

        if setting == 'net_encode':
            value = validate_net_encode(value)

        elif setting == 'ip_mode':
            value = validate_ip_mode(value)

        maps = SETTINGS_MAP[setting]
        assert isinstance(maps, dict)
        if serial_instance is None:
            # then is a group value, so no instance (like "/config/serial/max_port")
            api_path = copy.copy(maps["path"])
        else:  # else with instance (like "/config/serial/0/baud")
            api_path = maps["path"] % serial_instance
        assert isinstance(api_path, str)

        result = self.api.put(api_path, value)

        if self.logger is not None:
            self.logger.debug("Setting.put({0}, {1}) = {2}".format(api_path, value, result))

        return result

    def put_json(self, params):
        """
        assume params is like {"setting": "net_encode", "value": value}

        :param params: the JSONRPC params, decoded as Python
        :type params: dict

        """
        if "setting" not in params:
            raise ValueError("JSON PUT requires a 'setting' param")

        # this will raise a ValueError if not a valid name
        setting = self.validate_setting_name(params["setting"])

        maps = SETTINGS_MAP[setting]
        assert isinstance(maps, dict)

        if "validate" in maps:
            maps["validate"](params["value"])

        if "setting" not in params:
            raise ValueError("JSON PUT requires a 'setting' param")

        return

IP_MODE_UDP = 'udp'
IP_MODE_TCP = 'tcp'
IP_MODE_SSL = 'tls'
IP_MODE_LIST = ('udp', 'tcp', 'tls')


def validate_ip_mode(value):
    """
    validate the server port mode for the network socket

    :param value:
    :type value: str
    :return: True if okay, else throws exception
    :rtype: str
    """
    if value is None or value == "":
        # then reset to default
        value = SETTINGS_MAP["ip_mode"]["default"]

    value = value.lower().strip()
    value = value[:3]
    if value in ('ssl', 'tls'):
        value = IP_MODE_SSL
    elif value == 'udp':
        value = IP_MODE_UDP
    elif value == 'tcp':
        value = IP_MODE_TCP

    else:
        raise ValueError("setting 'ip_mode' must be in {}".format(IP_MODE_LIST))

    return value


NET_ENCODE_BINARY = 'binary'
NET_ENCODE_QUOTED = 'quoted'
NET_ENCODE_UNICODE = 'unicode'
NET_ENCODE_HEXASCII = 'hexascii'
NET_ENCODE_BASE64 = 'base64'
NET_ENCODE_ZIP = 'zip'
NET_ENCODE_GZIP = 'gzip'
NET_ENCODE_LIST = ('binary', 'quoted', 'unicode', 'hexascii', 'base64', 'zip', 'gzip')


def validate_net_encode(value):
    """
    validate the encoding format for the network socket

    - 'binary' (or 'raw') means raw 8-bi binary
    - 'ascii' (or utf8) means uncode strings
    - hexascii means each 8-bit value as 2 ascii hex values, so 0x40 is "40"
    - radix64 means each 2 x 8-bits as 3 ascii values

    :param value:
    :type value: str
    :return: True if okay, else throws exception
    :rtype: str
    """
    if value is None or value == "":
        # then reset to default
        value = SETTINGS_MAP["net_encode"]["default"]

    value = value.lower().strip()
    value = value[:3]
    if value in ('byt', 'bin', 'raw'):
        value = NET_ENCODE_BINARY

    elif value == 'quo':
        value = NET_ENCODE_QUOTED

    elif value in ('asc', 'uni', 'utf'):
        value = NET_ENCODE_UNICODE

    elif value == 'hex':
        value = NET_ENCODE_HEXASCII

    elif value in ('rad', 'bas', 'r64'):
        value = NET_ENCODE_BASE64

    else:
        raise ValueError("setting 'net_encode' must be in {}".format(NET_ENCODE_LIST))

    return value


SER_BAUD_LIST = (300, 600, 1200, 2400, 4800, 9600, 19200, 19200, 38400, 57600, 115200)


def validate_baud(value):
    """
    Validate the serial baud rate

    :param value:
    :type value: str or int
    :return: the validated value, else throws exception
    :rtype: int
    """
    if isinstance(value, str):
        value = int(value)

    if value not in SER_BAUD_LIST:
        raise ValueError("setting 'baud' must be in {}".format(SER_BAUD_LIST))

    return value


# a small amount of cheat, as serial.PARITY_NONE == 'N', but we want to validate just in case
SER_PARITY_MAPS = {
    'n': serial.PARITY_NONE,
    'e': serial.PARITY_EVEN,
    'o': serial.PARITY_ODD,
    'm': serial.PARITY_MARK,
    's': serial.PARITY_SPACE
}


def validate_parity(value):
    """
    Validate the serial parity

    :param value:
    :type value: str
    :return: the validated value, else throws exception
    :rtype: int
    """
    # we just look at first byte
    value = value[:1].upper()
    if value in SER_PARITY_MAPS:
        return SER_PARITY_MAPS[value]

    raise ValueError("setting 'parity' must be in {}".format(serial.PARITY_NAMES))


def validate_databits(value):
    """
    Validate the serial data bits, which is only 7 or 8

    :param value:
    :type value: str or int
    :return: the validated value, else throws exception
    :rtype: int
    """
    if isinstance(value, str):
        value = int(value)

    if value not in (serial.SEVENBITS, serial.EIGHTBITS):
        raise ValueError("setting 'databits' must be in (7, 8)")
    return value


def validate_stopbits(value):
    """
    Validate the serial data bits

    :param value:
    :type value: str, int, or float
    :return: the validated value, else throws exception
    :rtype: int
    """
    if isinstance(value, str):
        value = float(value)

    if value == serial.STOPBITS_ONE_POINT_FIVE:
        return serial.STOPBITS_ONE_POINT_FIVE
    value = int(value)
    if value not in (serial.STOPBITS_ONE, serial.STOPBITS_TWO):
        raise ValueError("setting 'stopbits' must be in (1, 1.5, 2)")
    return value


SER_FLOW_NONE = 'none'
SER_FLOW_HW = 'rts'
SER_FLOW_SW = 'xon'
SER_FLOW_LIST = (SER_FLOW_NONE, SER_FLOW_HW, SER_FLOW_SW)


def validate_flow_control(value):
    """
    Validate the serial data bits

    :param value:
    :type value: str or None
    :return: the validated value, else throws exception
    :rtype: int
    """
    if value is None:
        return SER_FLOW_NONE

    value = value.lower()
    if value not in SER_FLOW_LIST:
        raise ValueError("setting 'flow_control' must be in {0}".format(SER_FLOW_LIST))

    return value

SER_DTR_OFF = 'off'
SER_DTR_ON = 'on'
SER_DTR_CONN = 'connect'
SER_DTR_LIST = (SER_DTR_OFF, SER_DTR_ON, SER_DTR_CONN)


def validate_dtr_output(value):
    """
    Validate the initial DTR/DSR output setting

    :param value:
    :type value: str or None
    :return: the validated value, else throws exception
    :rtype: int
    """
    if value is None:
        value = SER_DTR_OFF

    value = value.lower()
    if value not in SER_DTR_LIST:
        raise ValueError("setting 'dtr_output' must be in {0}".format(SER_DTR_LIST))

    return value


SER_RTS_OFF = 'off'
SER_RTS_ON = 'on'
SER_RTS_LIST = (SER_RTS_OFF, SER_RTS_ON)


def validate_rts_output(value):
    """
    Validate the initial RTS/CTS output setting

    :param value:
    :type value: str or None
    :return: the validated value, else throws exception
    :rtype: int
    """
    if value is None:
        value = SER_RTS_OFF

    value = value.lower()
    if value not in SER_RTS_LIST:
        raise ValueError("setting 'rts_output' must be in {0}".format(SER_RTS_LIST))

    return value


SETTINGS_MAP = {
    "control_mode": {"path": "/config/serial/control_mode", "type": str, "default": "tcp",
                     "global": True, "validate": validate_ip_mode},
    "control_port": {"path": "/config/serial/control_port", "type": int, "default": 9001,
                     "global": True},
    "max_ports": {"path": "/config/serial/max_port", "type": int, "default": 1,
                  "global": True},

    "ip_mode": {"path": "/config/serial/%d/ip_mode", "type": str, "default": "tcp", "lower": True,
                "validate": validate_ip_mode},
    "ip_port": {"path": "/config/serial/%d/ip_port", "type": int, "default": 2101},
    "ser_port": {"path": "/config/serial/%d/ser_port", "type": str, "default": "COM1"},
    "net_encode": {"path": "/config/serial/%d/net_encode", "type": str, "default": "binary",
                   "validate": validate_net_encode},
    "product": {"path": "/config/serial/%d/product", "type": str, "default": "DTE"},
    "baud": {"path": "/config/serial/%d/baud", "type": int, "default": 9600,
             "validate": validate_baud},
    "parity": {"path": "/config/serial/%d/parity", "type": str, "default": 'None',
               "validate": validate_parity},
    "databits": {"path": "/config/serial/%d/databits", "type": str, "default": 'None',
                 "validate": validate_databits},
    "stopbits": {"path": "/config/serial/%d/stopbits", "type": str, "default": 'None',
                 "validate": validate_stopbits},
    "flow_control": {"path": "/config/serial/%d/flow_control", "type": str, "default": "None",
                     "validate": validate_flow_control},
    "dtr_output": {"path": "/config/serial/%d/dtr_output", "type": str, "default": "On",
                   "validate": validate_dtr_output},
    "rts_output": {"path": "/config/serial/%d/rts_output", "type": str, "default": "On",
                   "validate": validate_rts_output},
    "ser_publish_rate": {"path": "/config/serial/%d/ser_publish_rate", "type": str, "default": "15 sec",
                         "validate": validate_rts_output},
    "eoln": {"path": "/config/serial/%d/eoln", "type": str, "default": "\n"},
}
