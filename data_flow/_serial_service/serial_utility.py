__author__ = 'Lynn'


import binascii


from serial_settings import SerialSettings


# decode means net/bytes to local data
def decode_bytes_to_local(data, mode):
    """

    :param data:
    :param mode:
    :return:
    """
    if mode in DECODE_BYTES_TO_LOCAL:
        return DECODE_BYTES_TO_LOCAL[mode](data)

    raise ValueError("bad encoding method:{0}".format(mode))


def decode_binary(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_BINARY"""
    return data


def decode_unicode(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_UNICODE"""
    return data.decode()


def decode_quoted(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_QUOTED"""
    return binascii.b2a_qp(data)


def decode_hexascii(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_HEXASCII"""
    return binascii.b2a_hex(data)


def decode_base64(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_BASE64"""
    return binascii.b2a_base64(data)


DECODE_BYTES_TO_LOCAL = {
    SerialSettings.NET_ENCODE_BINARY: decode_binary,
    SerialSettings.NET_ENCODE_UNICODE: decode_unicode,
    SerialSettings.NET_ENCODE_QUOTED: decode_quoted,
    SerialSettings.NET_ENCODE_HEXASCII: decode_hexascii,
    SerialSettings.NET_ENCODE_BASE64: decode_base64,
}


# decode means local data to net/bytes
def encode_local_to_bytes(data, mode):
    """

    :param data:
    :param mode:
    :return:
    """
    if mode in ENCODE_BYTES_TO_LOCAL:
        return ENCODE_BYTES_TO_LOCAL[mode](data)

    raise ValueError("bad encoding method:{0}".format(mode))


def encode_binary(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_BINARY"""
    return data


def encode_unicode(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_UNICODE"""
    return data.encode()


def encode_quoted(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_QUOTED"""
    return binascii.a2b_qp(data)


def encode_hexascii(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_HEXASCII"""
    return binascii.a2b_hex(data)


def encode_base64(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_BASE64"""
    return binascii.a2b_base64(data)


ENCODE_BYTES_TO_LOCAL = {
    SerialSettings.NET_ENCODE_BINARY: encode_binary,
    SerialSettings.NET_ENCODE_UNICODE: encode_unicode,
    SerialSettings.NET_ENCODE_QUOTED: encode_quoted,
    SerialSettings.NET_ENCODE_HEXASCII: encode_hexascii,
    SerialSettings.NET_ENCODE_BASE64: encode_base64,
}

