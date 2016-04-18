__author__ = 'Lynn'


import binascii

import serial_settings


# decode means net/bytes to local data
def from_net_bytes_to_local(data, mode):
    """

    :param data:
    :param mode:
    :return:
    """
    if mode in DECODE_BYTES_TO_LOCAL:
        return DECODE_BYTES_TO_LOCAL[mode](data)

    raise ValueError("bad encoding method:{0}".format(mode))


def get_func_from_net(mode):
    """
    Given a mode, return the 'function' or method used to decode incoming data from wire

    :param mode:
    :type mode: str
    :return:
    """
    if mode in DECODE_BYTES_TO_LOCAL:
        return DECODE_BYTES_TO_LOCAL[mode]

    raise ValueError("bad encoding method:{0}".format(mode))


def from_net_binary(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_BINARY"""
    return data


def from_net_unicode(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_UNICODE"""
    return data.decode()


def from_net_quoted(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_QUOTED"""
    return binascii.a2b_qp(data).decode()


def from_net_hexascii(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_HEXASCII"""
    return binascii.a2b_hex(data).decode()


def from_net_base64(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_BASE64"""
    return binascii.a2b_base64(data).decode()


def from_net_zip(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_ZIP; unzip"""
    return binascii.a2b_base64(data).decode()


def from_net_gzip(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_GZIP; unzip"""
    return binascii.a2b_base64(data).decode()


DECODE_BYTES_TO_LOCAL = {
    serial_settings.NET_ENCODE_BINARY: from_net_binary,
    serial_settings.NET_ENCODE_UNICODE: from_net_unicode,
    serial_settings.NET_ENCODE_QUOTED: from_net_quoted,
    serial_settings.NET_ENCODE_HEXASCII: from_net_hexascii,
    serial_settings.NET_ENCODE_BASE64: from_net_base64,
    serial_settings.NET_ENCODE_ZIP: from_net_zip,
    serial_settings.NET_ENCODE_GZIP: from_net_gzip,
}


# decode means local data to net/bytes
def to_net_from_local(data, mode):
    """

    :param data:
    :param mode:
    :return:
    """
    if mode in ENCODE_BYTES_TO_LOCAL:
        return ENCODE_BYTES_TO_LOCAL[mode](data)

    raise ValueError("bad encoding method:{0}".format(mode))


def get_func_to_net(mode):
    """
    Given a mode, return the 'function' or method used to decode incoming data from wire

    :param mode:
    :type mode: str
    :return:
    """
    if mode in ENCODE_BYTES_TO_LOCAL:
        return ENCODE_BYTES_TO_LOCAL[mode]

    raise ValueError("bad encoding method:{0}".format(mode))


def to_net_binary(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_BINARY"""
    return data


def to_net_unicode(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_UNICODE"""
    return data.encode()


def to_net_quoted(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_QUOTED"""
    if isinstance(data, str):
        # we want it to be bytes/bytestring
        data = data.encode()
    return binascii.b2a_qp(data)


def to_net_hexascii(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_HEXASCII"""
    if isinstance(data, str):
        # we want it to be bytes/bytestring
        data = data.encode()
    return binascii.b2a_hex(data)


def to_net_base64(data):
    """Send encoders, when self.net_encode == SerialSettings.NET_ENCODE_BASE64"""
    if isinstance(data, str):
        # we want it to be bytes/bytestring
        data = data.encode()
    return binascii.b2a_base64(data)


def to_net_zip(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_BASE64"""
    return binascii.a2b_base64(data).decode()


def to_net_gzip(data):
    """Receive decoders, when self.net_encode == SerialSettings.NET_ENCODE_GZIP"""
    return binascii.a2b_base64(data).decode()


ENCODE_BYTES_TO_LOCAL = {
    serial_settings.NET_ENCODE_BINARY: to_net_binary,
    serial_settings.NET_ENCODE_UNICODE: to_net_unicode,
    serial_settings.NET_ENCODE_QUOTED: to_net_quoted,
    serial_settings.NET_ENCODE_HEXASCII: to_net_hexascii,
    serial_settings.NET_ENCODE_BASE64: to_net_base64,
    serial_settings.NET_ENCODE_ZIP: to_net_zip,
    serial_settings.NET_ENCODE_GZIP: to_net_gzip,
}
