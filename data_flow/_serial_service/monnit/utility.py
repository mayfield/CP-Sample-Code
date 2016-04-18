# misc utility routines for Monnit protocols

import time
import struct

# is 2010-01-01
MONNIT_EPOCH = time.mktime((2010, 1, 1, 0, 0, 0, 0, 0, 0))


def get_monnit_utc_float(now=None):
    """
    Get 'now' as float, seconds adjusted to match Monnit's epoch od 2010-Jan-01

    :param now: allow passing in fixed time.time() for testing
    :type now: float or None
    :return:
    :rtype: float
    """
    if now is None:
        now = time.time()
    return now - MONNIT_EPOCH


def get_monnit_utc_le32(now=None):
    """
    Get monnit 'now' as LE int packed as 4-bytes
    :param now: allow passing in fixed Monnit UTC for testing
    :type now: float or None
    :return:
    :rtype: bytes
    """
    if now is None:
        now = get_monnit_utc_float()
    return struct.pack("<I", int(now))


def parse_monnit_utc_le32(data):
    """
    :param data: the raw data from the media - if 0x00000000, then leave as zero!
    :type data: bytes
    :return:
    :rtype: float
    """
    x = struct.unpack("<I", data[0:4])[0]
    if x != 0:
        # then add the EPOCH
        x += MONNIT_EPOCH
    return float(x)


def format_timestamp(value, true_iso=False):
    """

    :param value: the source time, as linux or monnit
    :type value: float
    :param true_iso: T for "2015-12-18T19:32:27Z", or F for "2015-12-18 19:32:27 UTC"
    :return:
    """
    if value is None or value == 0:
        return "None"

    if value < 1000000000.0:
        # then is a Monnit value, so add back the EPOCH
        value += MONNIT_EPOCH

    if true_iso:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(value))
    else:  # else assume is 1970-1-1 epoch
        return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(value))


def convert_byte_sint(data):
    """
    :param data: the source time, as linux or monnit
    :type data: int
    :rtype: int
    """
    assert 0 <= data <= 255

    if data > 127:
        return -(256 - data)
    else:
        return data
