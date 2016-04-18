# File: data_types.py
# Desc: simple mapping the base class for the morsel project

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#

"""\
The data objects:

Attributes:
[
        self._required_keys = ['class', 'name', 'data_type']

Optional Attribute:
['description'] The user description, which is unicode. The description is usually something like
        "outdoor ambient temperature", or "the door switch on north wall".

['user_tag'] The user asset tag, which is unicode. The user asset tag is a user-assigned tag, such
        as "NE16273", which is used to identify something in other systems. It likely must be unique,
        however no uniqueness is enforced here!

"""

import common.parse_data as parse_data

# we limit Python types to more generic ones
MAP_TYPE = {
    int: float,
    float: float,
    str: str,
    bool: bool,
    tuple: list,
    list: list,
    type(None): type(None)
}

# JSON requires a string or numeric value - no Python types
MAP_TYPE_TO_JSON = {
    int: 'num',
    float: 'num',
    str: 'str',
    bool: 'bool',
    list: 'list',
    tuple: 'list',
    type(tuple): 'list',
    type(None): 'null'
}

# JSON offers a string value - no complex types
MAP_TYPE_FROM_JSON = {
    'num': float,
    'str': str,
    'bool': bool,
    'list': list,
    'null': type(None)
}

SPECIAL_NAME_CHAR = ('_', '-')


def data_type_python_to_internal(value):
    """
    Given a normal Python type, convert to one of our own required types.

    :param value: python type or variable
    :return:
    """
    if not isinstance(value, type):
        # if the user passed in a value, then take the type of it
        value = type(value)

    if value in MAP_TYPE:
        # if we could convert, then do so
        return MAP_TYPE[value]

    raise TypeError("This data type (%s) cannot be converted to internal" % value)


def data_type_export_to_json(value):
    """
    Given a our own required types, return a string for use in JSON transport.

    :param value: Morsel data type
    :return: string for use in JSON transport, like "num"
    :rtype: str
    """
    if value in MAP_TYPE_TO_JSON:
        # if we could convert, then do so
        return MAP_TYPE_TO_JSON[value]

    if not isinstance(value, type):
        # if the user passed in a value, then take the type of it
        value = type(value)
        return MAP_TYPE_TO_JSON[value]

    raise TypeError("This data type (%s) cannot be converted to JSON" % value)


def data_type_import_from_json(value: str):
    """
    Given a string for use in JSON transport, return our own internal type

    :param value: string for use in JSON transport, like "num"
    :return: our own internal type
    :rtype: type
    """
    if isinstance(value, str):
        value = value.lower()
        if value in MAP_TYPE_FROM_JSON:
            # if we could convert, then do so
            return MAP_TYPE_FROM_JSON[value]

    raise TypeError("This data type (%s) cannot be accepted from JSON" % value)


class Digital(int):

    @ staticmethod
    def validate(value):
        return bool(parse_data.parse_boolean(value))


class Numeric(float):

    @ staticmethod
    def validate(value):
        if type(value) in (str, bytes):
            # this handle the string padding, strip, etc
            return float(parse_data.parse_integer_or_float(value))

        if type(value) in (float, int):
            return float(value)

        raise TypeError("Numeric data type must be float or int")


class IndexString(str):
    """
    Our indexable string, with a reduced char set. Used for storage
    """

    @ staticmethod
    def validate(value):
        return validate_name(value)


def validate_name(value: str):
    """
    Validate (Convert & Test) the item name, return the name if okay, else throw an exception

    :param value: Morsel name
    :return:
    """
    # confirm boils down to the unicode subset we support
    value = validate_string(value)

    if len(value) < 1:
        # must be at least 1 character
        raise ValueError("validate_name " + "too short")

    for ch in value:
        if ch.isalnum():
            pass
        elif ch in SPECIAL_NAME_CHAR:
            # we only allow the '_' and '-' - no space, etc
            pass
        else:
            raise ValueError("validate_name " + "invalid:\"%s\"" % value)

    return value.lower()


class UserString(str):
    """
    Our UTF8 string, with a reduced char set
    """

    @ staticmethod
    def validate(value, none_to_empty_string=True):
        return validate_string(value, none_to_empty_string)


def validate_string(value: str, none_to_empty_string=True):
    """
    Validate (Test) a generic string item, return the string (as unicode) if okay, else throw an exception

    We block codes per RFC 3629 and MQTTv3.x, plus double quotes, and u'\x00'

    :param value: a generic string
    :return:
    """
    if value is None and none_to_empty_string:
        # print "Treat None as an 'empty string'"
        return u""

    if not isinstance(value, str):
        raise TypeError("validate_string " + "must be a string!")

    if not len(value):
        # print "although an 'empty string' is not technically value unicode, we allow for obvious reasons"
        return u""

    # then walk through an manually confirm some rules
    for ch in value:
        # validate per MQTT-v3.x limitations
        if ch in ('\"', '\\'):
            # don't allow the double quotes or escape, as it will confuse JSON
            pass

        elif chr(0x1F) < ch < chr(0x7F):
            # these are normal ASCII chars, as 0x00 to 0x1F are 'control' characters
            continue

        elif chr(0x9F) < ch < chr(0xD800):
            # these are normal Unicode chars, and 0xD800 to 0xDFFF are reserved for UTF-16
            continue

        elif chr(0xD8FF) < ch < chr(0xFFFF):
            # these are more normal Unicode chars, and 0xFFFF is defined as bad?
            continue

        raise ValueError("validate_string " + "invalid code:U+0x%04X" % ord(ch))

    return value
