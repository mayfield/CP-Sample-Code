def format_bytes(tag, data):
    """

    :param tag:
    :type tag: None or str
    :param data:
    :type data: bytes or list
    :return:
    :rtype: str
    """
    if tag is not None:
        result = tag
    else:
        result = tag

    if data is None or len(data) == 0:
        result += "[000]"

    else:
        result += "[%03d]" % len(data)
        for by in data:
            result += "%02X " % by

    return result
