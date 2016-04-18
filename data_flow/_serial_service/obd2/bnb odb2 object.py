import struct
import logging
import sys

__author__ = 'Lynn'


QUALITY_GOOD = 0
QUALITY_UNDER_RANGE = 0x10
QUALITY_OVER_RANGE = 0x20


DATA_DEFS = [
    {'cmd': 0x00, 'nam': 'Vehicle Speed', 'siz': 2, 'uom': 'MPH', 'sca': 0.0024390243902439,
     'min': 0, 'max': 160},
    {'cmd': 0x01, 'nam': 'Engine Speed', 'siz': 2, 'uom': 'RPM', 'sca': 0.25,
     'min': 0, 'max': 16384},
    {'cmd': 0x02, 'nam': 'Throttle Position', 'siz': 2, 'uom': '%', 'sca': 0.0015267175572519,
     'min': 0, 'max': 100},
    {'cmd': 0x03, 'nam': 'Odometer', 'siz': 4, 'uom': 'miles', 'sca': None,
     'min': 0, 'max': 999992},
    {'cmd': 0x04, 'nam': 'Fuel Level', 'siz': 2, 'uom': '%', 'sca': 0.0015267175572519,
     'min': 0, 'max': 100},
    {'cmd': 0x05, 'siz': None},
    {'cmd': 0x06, 'siz': None},
    {'cmd': 0x07, 'nam': 'Engine Coolant Temp', 'siz': 2, 'uom': 'F', 'sca': '(%d * 1/64) - 40',
     'min': -40, 'max': 983},
    {'cmd': 0x08, 'nam': 'Ignition Status', 'siz': 2, 'if_0': True, 'uom_t': 'Off', 'uom_f': 'On'},
    {'cmd': 0x09, 'nam': 'MIL Status', 'siz': 2, 'if_0': True, 'uom_t': 'Off', 'uom_f': 'On'},
    {'cmd': 0x0A, 'siz': None},
    {'cmd': 0x0B, 'siz': None},
    {'cmd': 0x0C, 'nam': 'Fuel Rate', 'siz': 2, 'uom': 'GPH', 'sca': 1 / 2185,
     'min': 0, 'max': 29.99},
    {'cmd': 0x0D, 'nam': 'Battery Voltage', 'siz': 2, 'uom': 'Volts', 'sca': 1 / 3641,
     'min': 0, 'max': 18},
    {'cmd': 0x0E, 'nam': 'PTO Status', 'siz': 2, 'if_0': True, 'uom_t': 'Off', 'uom_f': 'On'},
    {'cmd': 0x0F, 'nam': 'Seat Belt Fastened', 'siz': 2, 'if_0': True, 'uom_t': 'Fastened', 'uom_f': 'Not Fastened'},
    {'cmd': 0x10, 'nam': 'Misfire Monitor', 'siz': 2, 'if_0': True, 'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x11, 'nam': 'Fuel System Monitor', 'siz': 2, 'if_0': True, 'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x12, 'nam': 'Comprehensive Component Monitor', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x13, 'nam': 'Catalyst Monitor', 'siz': 2, 'if_0': True, 'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x14, 'nam': 'Heated Catalyst Monitor', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x15, 'nam': 'Evaporative System Monitor', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x16, 'nam': 'Secondary Air System Monitor', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x17, 'nam': 'A/C System Refrigerant Monitor', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x18, 'nam': 'Oxygen Sensor Monitor', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x19, 'nam': 'Oxygen Sensor Heater Monitor', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x1A, 'nam': 'Monitor (0x1A)', 'siz': 2, 'if_0': True,
     'uom_t': 'Complete', 'uom_f': 'Not Complete'},
    {'cmd': 0x1B, 'nam': 'Brake Switch Status', 'siz': 2, 'if_0': True, 'uom_t': 'Pressed', 'uom_f': 'Not Pressed'},
    {'cmd': 0x1C, 'nam': 'Ambient Air Temp', 'siz': 2, 'uom': 'F', 'sca': '(%d * 1/64) - 40',
     'min': -40, 'max': 983},
    {'cmd': 0x1D, 'siz': None},
    {'cmd': 0x1E, 'siz': None},
    {'cmd': 0x1F, 'siz': None},
    {'cmd': 0x20, 'siz': None},
    {'cmd': 0x21, 'siz': None},
    {'cmd': 0x22, 'nam': 'Trip Odometer', 'siz': 4, 'uom': 'Miles', 'sca': 0.1,
     'min': 0, 'max': 999992},
    {'cmd': 0x23, 'nam': 'Trip Fuel Consumption', 'siz': 4, 'uom': 'Gal', 'sca': 0.0078125,
     'min': 0, 'max': 999992},
    {'cmd': 0x24, 'nam': 'Distance since DTC cleared', 'siz': 4, 'uom': 'Miles', 'sca': None,
     'min': 0, 'max': 999992},
    {'cmd': 0x25, 'nam': 'Transmission Fluid Temp', 'siz': 2, 'uom': 'F', 'sca': '(%d * 1/64) - 40',
     'min': -40, 'max': 983},
    {'cmd': 0x26, 'nam': 'Oil Life Remaining', 'siz': 2, 'uom': '%', 'sca': 0.002, 'min': 0, 'max': 100},
    # these 2 are special
    {'cmd': 0x27, 'nam': 'Tire Pressure Monitoring Status', 'siz': None},
    {'cmd': 0x28, 'nam': 'Tire Pressure', 'siz': 6, 'uom': 'PSI'},
]


TIRE_PRES_NAMES = ('Left Front', 'Right Front', 'Outer Left Rear', 'Inner Left Rear',
                   'Inner Right Rear', 'Outer Right Rear')

"""
0x27 Tire Pressure Monitoring Status 8 Bytes Normal/Abnormal (see below)
0x28 Tire Pressures 6 Bytes PSI 0-255 each
"""


def _parse_parameter_data(cmd, data):
    """

    :param cmd: the command expected
    :type cmd: int
    :param data: the bytes from the protocol
    :type data: int or bytes
    :return: value, quality bits
    :rtype: dict
    """

    # see if command is valid
    if not 0 <= cmd < len(DATA_DEFS):
        raise ValueError("BnB ODBII - bad parameter value %d, not in range(0,4)")

    # handle the special values
    if cmd == 0x27:
        # 'nam': 'Tire Pressure Monitoring Status',
        return parse_tire_pres_monitoring_status(data)

    elif cmd == 0x28:
        # 'nam': 'Tire Pressure',
        return parse_tire_pres(data)

    _defs = DATA_DEFS[cmd]
    assert _defs['cmd'] == cmd

    # {'cmd': 0x00, 'nam': 'Vehicle Speed', 'siz': 2, 'uom': 'MPH', 'sca': 0.0024390243902439,
    #  'min': 0, 'max': 160},

    x = _defs['siz']
    if x == 1:
        data = data[0]
    elif x == 2:
        data = struct.unpack(">H", data[0:2])[0]
    elif x == 4:
        data = struct.unpack(">I", data[0:4])[0]
    elif x == 8:
        data = struct.unpack(">Q", data[0:8])[0]
    elif x is None:
        raise AttributeError("BnB ODBII - command not known")
    else:
        raise ValueError("BnB ODBII - byte count must be in (1,2,4,8)")

    quality = QUALITY_GOOD

    if 'if_0' in _defs:
        # {'cmd': 0x09, 'nam': 'MIL Status', 'siz': 2, 'if_0': True, 'uom_t': 'Off', 'uom_f': 'On'},
        if data == 0:
            data = _defs['if_0']
        elif data == 1:
            data = not(_defs['if_0'])
        else:
            raise ValueError("BnB ODBII - bool data not 0 or 1")

        if data:
            uom = _defs['uom_t']
        else:
            uom = _defs['uom_f']

    else:
        x = _defs['sca']
        if x is None:
            # then data == raw, there is no scale or adjustment
            pass
        elif isinstance(x, str):
            # then is like '(%d * 1/64) - 40'
            data = eval(x % data)
        else:
            # else is scaler/multiplier like 0.25
            data *= _defs['sca']

        if _defs['min'] is not None and data < _defs['min']:
            quality = QUALITY_UNDER_RANGE

        elif _defs['max'] is not None and data < _defs['max']:
            quality = QUALITY_OVER_RANGE

        uom = _defs['uom']

    return {'value': data, 'uom': uom, 'quality': quality}


def parse_tire_pres_monitoring_status(data):
    """

    :param data: the bytes from the protocol
    :type data: bytes
    :rtype: dict
    """
    if len(data) != 8:
        #
        raise ValueError("BnB ODBII - tire pres monitor status data count is wrong")

    value = []
    for x in data:
        if x == b'\x00':
            value.append(False)
        elif x == b'\x01':
            value.append(True)
        else:
            raise ValueError("BnB ODBII - bool data not 0 or 1")

    return {'value': value, 'quality': QUALITY_GOOD}


def parse_tire_pres(data):
    """

    :param data: the bytes from the protocol
    :type data: bytes
    :rtype: dict
    """
    if len(data) != 6:
        #
        raise ValueError("BnB ODBII - tire pres data count is wrong")

    value = []
    for x in data:
        value.append(int(x))

    return {'value': value, 'quality': QUALITY_GOOD}


def test_data_examples():
    tests = [
        {'cmd': 0x00, 'data': b'\x68\x1A', 'result': 65.0},
        {'cmd': 0x01, 'data': b'\x2E\xE0', 'result': 3000.0},
        {'cmd': 0x02, 'data': b'\x2E\xE0', 'result': 18.32},
        {'cmd': 0x03, 'data': b'\x00\x00\xE3\x0D', 'result': 58125},
        {'cmd': 0x04, 'data': b'\x5C\x1A', 'result': 35.99},
        {'cmd': 0x05, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x06, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x07, 'data': b'\x37\x00', 'result': 180.0},
        {'cmd': 0x08, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x08, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x09, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x09, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x0A, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x0B, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x0C, 'data': b'\x64\x32', 'result': 11.74},
        {'cmd': 0x0D, 'data': b'\xB2\x52', 'result': 12.538},
        {'cmd': 0x0E, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x0E, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x0F, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x0F, 'data': b'\x00\x01', 'result': False},

        {'cmd': 0x10, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x10, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x11, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x11, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x12, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x12, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x13, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x13, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x14, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x14, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x15, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x15, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x16, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x16, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x17, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x17, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x18, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x18, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x19, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x19, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x1A, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x1A, 'data': b'\x00\x01', 'result': False},
        {'cmd': 0x1B, 'data': b'\x00\x00', 'result': True},
        {'cmd': 0x1B, 'data': b'\x00\x01', 'result': False},

        {'cmd': 0x1C, 'data': b'\x37\x00', 'result': 180.0},
        {'cmd': 0x1D, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x1E, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x1F, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x20, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x21, 'data': b'\x00\x00', 'result': AttributeError},
        {'cmd': 0x22, 'data': b'\x00\x00\xE3\x0D', 'result': 5812.5},
        {'cmd': 0x23, 'data': b'\x00\x00\x1F\xC0', 'result': 63.5},
        {'cmd': 0x24, 'data': b'\x00\x00\x02\x45', 'result': 581},
        {'cmd': 0x25, 'data': b'\x4B\x00', 'result': 260.0},
        {'cmd': 0x26, 'data': b'\x5D\xC0', 'result': 48.0},
    ]

    for test in tests:

        try:
            logger.debug(repr(test))
            value, uom, quality = _parse_parameter_data(test['cmd'], test['data'])

            expect = test['result']
            if abs(value - expect) > 0.1:
                logger.error('output_channel_name not as expected in %s', test)
                logger.error('  value: %s', value)
                logger.error(' expect: %s', expect)
                return False

        except AttributeError:
            if test['result'] != AttributeError:
                raise
            else:
                pass

    logger.info('   ... was Okay')
    logger.info(' ')
    return True


if __name__ == '__main__':
    global logger

    logger = logging.getLogger('test')
    logging.basicConfig()

    # _logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    test_all = False
    if test_all:
        logger.setLevel(logging.INFO)

    if True or test_all:
        if not test_data_examples():
            logger.error('TEST FAILED!')
            sys.exit(-1)
