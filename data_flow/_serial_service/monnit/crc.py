# file: crc.py = Monnit serial CRC routine


def crc_isvalid(message):
    """
    Given the message, which MUST include the CRC, calc CRC and compare to last byte

    :param message:
    :type message: bytes
    :return: True if correct CRC appended, else will throw ValueError
    :rtype: bytes
    """
    from monnit.protocol import form_isvalid, MonnitProtocolError

    # expect_length is without the CRC byte
    expect_length = form_isvalid(message)

    if expect_length != len(message) - 1:
        # then we're missing the CRC
        raise MonnitProtocolError("message lacks CRC")

    crc = crc_calculate(message)
    if crc != message[-1]:
        raise MonnitProtocolError("message has bad CRC. saw:%02X expect:%02X" % (message[-1], crc))
    return True


def crc_append(message):
    """
    Given the message (with or without CRC), calc CRC and crc_append as last byte

    Any old (or unknown) byte in the CRC offset is discarded.

    :param message:
    :type message: bytes
    :return: message passed in, with correct CRC appended
    :rtype: bytes
    """
    from monnit.protocol import form_isvalid

    # expect_length is without the CRC byte
    expect_length = form_isvalid(message)

    if expect_length == len(message) - 1:
        # then remove old/unknown CRC
        message = message[:-1]

    message += bytes([crc_calculate(message)])
    return message


def crc_calculate(message):
    """
    Given the message, return CRC as an int.

    The protocol defines the bytes in CRC as:
    <0xC5><LEN>crc data is here<CRC>

    :param message:
    :type message: bytes
    :return: the CRC as int of messages passed in
    :rtype: int
    """
    from monnit.protocol import form_isvalid

    expect_length = form_isvalid(message)

    crc = 0
    for i in range(2, expect_length):
        # if message is incorrect length, we'll might throw IndexError
        crc = _add_byte(crc, message[i])
    return crc


def _add_byte(crc, next_byte):
    """
    Given a building CRC, add 1 more byte to it

    :param crc: the initial CRC, which starts as 0
    :type crc: int
    :param next_byte:
    :type next_byte: int
    :return: the resulting CRC after one-more byte calc
    :rtype: int
    """
    crc = (crc ^ next_byte) & 0xFF
    for j in range(0, 8):
        if (crc & 0x80) == 0x80:
            crc = ((crc << 1) & 0xFF) ^ 0x97
        else:
            crc <<= 1
        crc &= 0xFF
    return crc
