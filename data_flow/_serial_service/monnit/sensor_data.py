"""
Each sensor has its own data format. This object parses (or builds) the data, mapping binary
to keyed data
"""

import struct
# import logging
# logging.debug("info {0}".format(info))


class MonnitSensorData(object):

    TYPE_INFO = {
        2: {'code': 2, 'name': 'temperature', 'fmt': '%0.1f %s'},
        3: {'code': 3, 'name': 'dry contact', 'fmt': '%s(%s)'},
        9: {'code': 9, 'name': 'open closed', 'fmt': '%s(%s)'},
        23: {'code': 23, 'name': 'PIR motion', 'fmt': '%s(%s)'},
        43: {'code': 43, 'name': 'humidity', 'fmt': '%0.1f %s'},
    }

    initialized = False

    def __init__(self):
        if not MonnitSensorData.initialized:
            # push the callbacks into the static data structure
            # six bogus type check warnings below, so suppress
            #  - example: MonnitSensorData.TYPE_INFO[2] is dict/keyed, ['fnc'] is okay
            # noinspection PyTypeChecker
            MonnitSensorData.TYPE_INFO[2]['fnc'] = self.parse_02_temperature
            # noinspection PyTypeChecker
            MonnitSensorData.TYPE_INFO[3]['fnc'] = self.parse_03_dry_contact
            # noinspection PyTypeChecker
            MonnitSensorData.TYPE_INFO[9]['fnc'] = self.parse_09_open_close
            # noinspection PyTypeChecker
            MonnitSensorData.TYPE_INFO[23]['fnc'] = self.parse_23_pir_motion
            # noinspection PyTypeChecker
            MonnitSensorData.TYPE_INFO[43]['fnc'] = self.parse_43_humidity

            # noinspection PyTypeChecker
            MonnitSensorData.TYPE_INFO[43]['fmt'] = self.show_43_humidity

            MonnitSensorData.initialized = True

        self._attrib = {'degf': True}

        return

    def parse_any(self, result, data):
        """
        We assume this is data-log payload++, so
        data[0] = LSB of sensor type
        data[1] = MSB of sensor type
        data[2] = state
        data[+] = optional data (per sensor type)

        :param result: the building keyed data
        :type result: dict
        :param data: the raw binary data, which MUST start with the LE-16 sensor type.
        :type data: bytes
        :return:
        """
        if len(data) < 3:
            raise ValueError("Monnit Sensor data too short - less than 3 bytes")

        # Sensor Type, 2-byte LE
        result['sensor_type'] = struct.unpack("<H", data[0:2])[0]

        # Sensor State, 1-byte
        result['sensor_state'] = data[2]

        # Sensor Data, ?-byte
        if len(data) > 3:
            result['sensor_data'] = data[3:]
        else:
            result['sensor_data'] = None

        if result['sensor_type'] in self.TYPE_INFO:
            # then is known type, so parse the
            info = self.TYPE_INFO[result['sensor_type']]
            assert isinstance(info, dict)
            result = info['fnc'](result)

        return result

    def show_any(self, result):
        """
        Given a parsed keyed dict, return a string

        :param result: the building keyed data
        :type result: dict
        :return:
        """
        fmt = "%s %s"
        if result['sensor_type'] in self.TYPE_INFO:
            # then is known type, so parse the
            info = self.TYPE_INFO[result['sensor_type']]
            assert isinstance(info, dict)
            if 'fmt' in info:
                fmt = info['fmt']

                if not isinstance(fmt, str):
                    # then assume has custom callback
                    return fmt(result)

        # else do simple formatting of 1 value and UOM
        return fmt % (result['sensor_value1'], result['sensor_uom1'])

    def parse_02_temperature(self, result: dict):
        """
        The type specific data parsing
        :param result:
        :return:
        """
        from monnit.protocol import MonnitProtocolDataError

        assert result['sensor_type'] == 2

        # result['sensor_state'] - for now, leave as is

        # Sensor Data, ?-byte
        data = result['sensor_data']
        if len(data) != 2:
            raise MonnitProtocolDataError("Sensor03 expects 2 bytes data, saw %d" % len(data))

        # data[0-1] = S16 int to be div by 10
        x = struct.unpack("<h", data[0:2])[0] / 10.0

        if self._attrib.get('degf', False):
            # then convert to Degree F
            result['sensor_value1'] = round((x * 1.8) + 32, 2)
            result['sensor_uom1'] = 'F'
        else:  # else leave as Degree C
            result['sensor_value1'] = x
            result['sensor_uom1'] = 'C'

        return result

    def parse_03_dry_contact(self, result: dict):
        """
        The type specific data parsing
        :param result:
        :return:
        """
        from monnit.protocol import MonnitProtocolDataError

        assert result['sensor_type'] == 3

        # result['sensor_state'] - for now, leave as is

        # Sensor Data, ?-byte - spec says 2 bytes, but reality is only 1!
        data = result['sensor_data']
        if len(data) not in (1, 2):
            raise MonnitProtocolDataError("Sensor03 expects 2 bytes data, saw %d" % len(data))

        # data[0] = 0x00 or 0x01
        # data[1] is always zero
        # the MEANING of 0 or 1 is mangled by sensor config - def is 0=open, 1=close
        x = bool(data[0] == 1)
        result['sensor_value1'] = x

        if self._attrib.get('invert', False):
            # then inverted tags
            x = not x

        if x:
            result['sensor_uom1'] = 'closed'
        else:
            result['sensor_uom1'] = 'open'

        return result

    def parse_09_open_close(self, result: dict):
        """
        The type specific data parsing
        :param result:
        :return:
        """
        from monnit.protocol import MonnitProtocolDataError

        assert result['sensor_type'] == 9

        # result['sensor_state'] - for now, leave as is

        # Sensor Data, ?-byte
        data = result['sensor_data']
        if len(data) != 2:
            raise MonnitProtocolDataError("Sensor09 expects 2 bytes data, saw %d" % len(data))

        # data[0] = 0x00 or 0x01
        # data[1] is always zero
        # the MEANING of 0 or 1 is mangled by sensor config - def is 0=open, 1=close
        x = bool(data[0] == 1)
        result['sensor_value1'] = x

        if self._attrib.get('invert', False):
            # then inverted tags
            x = not x

        if x:
            result['sensor_uom1'] = 'closed'
        else:
            result['sensor_uom1'] = 'open'

        return result

    @staticmethod
    def parse_23_pir_motion(result: dict):
        """
        The type specific data parsing
        :param result:
        :return:
        """
        from monnit.protocol import MonnitProtocolDataError

        assert result['sensor_type'] == 23

        # result['sensor_state'] - for now, leave as is

        # Sensor Data, ?-byte
        data = result['sensor_data']
        if len(data) != 1:
            raise MonnitProtocolDataError("Sensor23 expects 1 byte data, saw %d" % len(data))

        # data[0] = 0=no motion, 1=detected
        x = bool(data[0] == 1)
        result['sensor_value1'] = x

        if x:
            result['sensor_uom1'] = 'motion detected'
        else:
            result['sensor_uom1'] = 'no motion'

        return result

    def parse_43_humidity(self, result: dict):
        """
        The type specific data parsing
        :param result:
        :return:
        """
        from monnit.protocol import MonnitProtocolDataError

        assert result['sensor_type'] == 43

        # result['sensor_state'] - for now, leave as is

        # Sensor Data, ?-byte
        data = result['sensor_data']
        if len(data) != 4:
            raise MonnitProtocolDataError("Sensor03 expects 2 bytes data, saw %d" % len(data))

        # data[0-1] = S16 int TEMP, to be div by 100
        # data[2-3] = S16 int HUM, to be div by 100
        x = struct.unpack("<h", data[0:2])[0] / 100.0

        if self._attrib.get('degf', False):
            # then convert to Degree F
            result['sensor_value2'] = round((x * 1.8) + 32, 2)
            result['sensor_uom2'] = 'F'
        else:  # else leave as Degree C
            result['sensor_value2'] = x
            result['sensor_uom2'] = 'C'

        x = struct.unpack("<h", data[2:4])[0] / 100.0
        result['sensor_value1'] = x
        result['sensor_uom1'] = '%RH'

        return result

    @staticmethod
    def show_43_humidity(result: dict):
        """
        The type specific data parsing
        :param result:
        :return:
        """
        assert result['sensor_type'] == 43

        return "%0.1f %s @ %0.1f %s" % (result['sensor_value1'], result['sensor_uom1'],
                                        result['sensor_value2'], result['sensor_uom2'])
