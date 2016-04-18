#
#        File: CRC16.PY
#              CRC-16 (reverse) table lookup for Modbus or DF1
#
#     Project: Modbus
#      Author: Lynn August Linse, based on method used by XMODEM
#    Language: Python 2.3
#
#     History: 2003Jun17 - Port from VB version
#

INITIAL_CRC_MODBUS = 0xFFFF
INITIAL_CRC_DF1 = 0x0000

table = tuple()


def init_table():
    """
    Initialize the CRC-16 lookup table as a tuple
    """
    global table

    if (len(table) == 256) and (table[1] == 49345):
        # print("Table already init!")
        return
    
    lst = []
    i = 0
    while i < 256:
        data = (i << 1)
        _crc = 0
        j = 8
        while j > 0:
            data >>= 1
            if (data ^ _crc) & 0x0001:
                _crc = (_crc >> 1) ^ 0xA001
            else:
                _crc >>= 1
            j -= 1
            
        lst.append(_crc)
        # print("entry %d = %x" % (i, lst[i]))
        i += 1

    table = tuple(lst)
    return


def calc_byte(by: int, crc_in: int):
    """
    given a Byte, Calc a modbus style CRC-16 by look-up table
    :param by: the next byte
    :param crc_in: the previous (or initial) CRC
    :rtype: int
    """
    init_table()

    crc_in = (crc_in >> 8) ^ table[(crc_in ^ int(by)) & 0xFF]
    return crc_in & 0xFFFF


def calc_byte_array(bya: bytes, crc_in: int):
    """
    given a ByteArray, Calc a modbus style CRC-16 by look-up table

    :param bya: the byte string
    :param crc_in: the previous (or initial) CRC
    :rtype: int
    """
    init_table()

    # print "bya = ", list(bya)
    for by in bya:
        crc_in = (crc_in >> 8) ^ table[(crc_in ^ int(by)) & 0xFF]
        # print(" crc_in=%x" % crc_in)
    return crc_in


def append_byte_array(bya: bytes, crc_in: int):
    """
    given a ByteArray, Calc a modbus style CRC-16 by look-up table

    :param bya: the byte string
    :param crc_in: the previous (or initial) CRC
    :rtype: bytes
    """
    working_crc = calc_byte_array(bya, crc_in)
    return bytearray(bya) + bytes([working_crc & 0xFF, (working_crc >> 8) & 0xFF])

if __name__ == '__main__':

    import binascii
    
    init_table()    

    # test Modbus
    print("testing Modbus messages with crc16.py")

    crc = INITIAL_CRC_MODBUS
    packet = b"\xEA\x03\x00\x00\x00\x64"
    for x in packet:
        crc = calc_byte(x, crc)
    if crc != 0x3A53:
        print("test case #a1: BAD - ERROR - FAILED!")
        print("expect:0x3A53 but saw 0x%x" % crc)
    else:
        print("test case #1a: Okay")

    # repeat above, but with the single byte_array call
    crc = calc_byte_array(packet, INITIAL_CRC_MODBUS)
    if crc != 0x3A53:
        print("test case #1b: BAD - ERROR - FAILED!")
        print("expect:0x3A53 but saw 0x%x" % crc)
    else:
        print("test case #1b: Okay")

    # repeat above, but return the array with CRC appended
    expect = b"\xEA\x03\x00\x00\x00\x64\x53\x3A"
    result = append_byte_array(packet, INITIAL_CRC_MODBUS)
    if result != expect:
        print("test case #1c: BAD - ERROR - FAILED!")
        print("expect:{0}".format(binascii.hexlify(expect)))
        print("result:{0}".format(binascii.hexlify(result)))
    else:
        print("test case #1c: Okay")

    packet = b"\x4b\x03\x00\x2c\x00\x37"
    crc = calc_byte_array(packet, INITIAL_CRC_MODBUS)
    if crc != 0xbfcb:
        print("test case #2: BAD - ERROR - FAILED!")
        print("expect:0xBFCB but saw 0x%x" % crc)
    else:
        print("test case #2: Okay")

    packet = b"\x0d\x01\x00\x62\x00\x33"
    crc = calc_byte_array(packet, INITIAL_CRC_MODBUS)
    if crc != 0x0ddd:
        print("test case #3: BAD - ERROR - FAILED!")
        print("expect:0x0DDD but saw 0x%x" % crc)
    else:
        print("test case #3: Okay")

    print()
    print("testing DF1 messages with crc16.py")
    
    packet = b"\x07\x11\x41\x00\x53\xB9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    # DF1 uses same algorithm - just starts with CRC=0x0000 instead of 0xFFFF
    crc = calc_byte_array(packet, INITIAL_CRC_DF1)
    crc = calc_byte(0x03, crc)
    if crc != 0x4C6B:
        print("test case #4: BAD - ERROR - FAILED!")
        print("expect:0x4C6B but saw 0x%x" % crc)
    else:
        print("test case #4: Okay")
