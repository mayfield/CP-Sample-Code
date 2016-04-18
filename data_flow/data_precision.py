# simple data precision routines
#

PRECISION_LIST = (0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)
PRECISION_FORMAT = {0.0001: "%0.4f", 0.001: "%0.3f", 0.01: "%0.2f",
                    0.1: "%0.1f",
                    1.0: "%d", 10.0: "%d", 100.0: "%d", 1000.0: "%d"}
PRECISION_REDUCE = {0.0001: 4, 0.001: 3, 0.01: 2, 0.1: 1, 1.0: 0, 10.0: -1,
                    100.0: -2, 1000.0: -3}


def validate_precision_value(precision):
    """
    Given a precision, confirm if it is supported, in set
    (0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)

    :param precision:
    :type precision: float
    :return: True if the precision value is as expected
    :rtype: bool
    """
    return bool(precision in PRECISION_LIST)


def get_precision_string_format(precision):
    """
    Given a precision for a value, return a typical Python format string.
    For example, a precision of 0.01
    means we use "%0.2f", so 73.2567 prints as "73.26"

    :param precision:
    :type precision: float
    :return: a typical Python format string
    :rtype: str
    """
    value = PRECISION_FORMAT.get(precision, None)
    if value is None:
        raise ValueError(
            "get_precision_string_format(%s) is not a valid precision input",
            precision)

    return value


def use_precision_to_reduce_value(precision: float, data):
    """
    Given a precision for a value, return a float 'rounded' down as required

    :param precision:
    :param data: the value to reduce
    :type data: int or float
    :return: the first isolated INT as int, or FLOAT as float
    :rtype: int or float
    """
    value = PRECISION_REDUCE.get(precision, None)
    if value is None:
        raise ValueError(
            "use_precision_to_reduce_value(%s) is not a valid precision input",
            precision)

    data = round(float(data), value)
    return data


def use_precision_to_string(precision: float, data):
    """
    Given a precision for a value, return a formatted string with value
    'rounded' down as required

    :param precision:
    :param data: the value to reduce
    :type data: int or float
    :return: the first isolated INT as int, or FLOAT as float
    :rtype: int or float
    """
    reduced_value = use_precision_to_reduce_value(precision, data)
    format_string = PRECISION_FORMAT.get(precision, None)

    return format_string % reduced_value
