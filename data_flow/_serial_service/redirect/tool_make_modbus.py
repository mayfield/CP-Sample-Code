__author__ = 'Lynn'

import redirect.crc16 as crc


def make_hex_string(source: bytes):
    x = ''
    for by in source:
        x += '\\x%02X' % by

    return x

if __name__ == '__main__':

    crc.init_table()

    for value in range(0, 256):
        # make the raw Modbus request
        request = bytes([0x01, 0x03, 0x00, value, 0x00, 0x01])
        request = crc.append_byte_array(request, crc.INITIAL_CRC_MODBUS)

        message = '    b\"' + make_hex_string(request) + '\", '
        print(message)

    print()

    for value in range(0, 256):
        # make the raw Modbus request
        response = bytes([0x01, 0x03, 0x02, value, value])
        response = crc.append_byte_array(response, crc.INITIAL_CRC_MODBUS)

        message = '    b\"' + make_hex_string(response) + '\", '
        print(message)
