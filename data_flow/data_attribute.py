# File: data_attribute.py
# Desc: data attribute handlers - it doesn't save anything, but manages the attributes

from data.data_types import IndexString, UserString, Digital, Numeric, validate_string, validate_name
import data.data_types as data_types
from data.data_color import DataColor
import common.parse_data as parse_data
from common.parse_duration import TimeDuration

__version__ = "1.1.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
# 1.1.0: 2015-Aug Lynn
#       *
#


class DataAttributeHandler(object):
    """
    A template (or prototype) for any object.

    ['data_name'] = a unique indexable name for this template (is not shared with data object)
    ['display_name'] = the UTF8 string, used as default for data objects linked to template
    ['display_color'] = the background color (or if tuple, as (background, foreground)
    ['font_scale'] = the color to show when value is False (like Red or Green)
    ['data_type'] = a value in DATA_TYPE_LIST
    ['description'] = the UTF8 string, used as default for data objects linked to template
    ['value_type'] = the python value of the data
    ['failsafe'] = a safe default value
    ['attach_gps'] = if GPS coordinates should be attached

    [source][owner_token][children] are always data object instance only

    It includes a converter to 'import' data, possibly modifying it and returning a data_type and uom
    """

    BASE_STATIC_ATTRIBUTES = ('data_name', 'display_name', 'display_color', 'font_scale', 'data_type',
                              'description', 'value_type', 'failsafe', 'attach_gps', 'read_only')

    BASE_DYNAMIC_ATTRIBUTES = ('source', 'owner_token', 'health')

    BASE_MAPS = {
        'data_name': {'data_type': IndexString},
        'display_name': {'data_type': UserString},
        'description': {'data_type': UserString},
        'display_color': {'data_type': DataColor},
        'font_scale': {'data_type': Numeric},
        'data_type': {'data_type': str, 'can_clear': False},
        'value_type': {'data_type': type, 'can_clear': False},
        'failsafe': {'data_type': None},
        'attach_gps': {'data_type': Digital},
        'read_only': {'data_type': Digital},

        'source': {'data_type': None},
        'owner_token': {'data_type': None},
        'health': {'data_type': float},
    }

    DATA_TYPE_LIST = ('base', 'string', 'digital', 'gps', 'analog')

    FONT_SCALE_LIST = (50, 75, 100, 125, 150)

    def __init__(self):
        return

    def set_attribute(self, attrib: dict, name: str, value):
        """
        load one base attributes

        :param attrib: the collection (dict) to update
        :param name: the attribute keyword / name
        :param value: the value to set
        :return: True if attribute handled, else False or exception thrown
        :rtype: bool
        """
        if not isinstance(attrib, dict):
            raise TypeError("Attrib parameter must be a type dict")

        if not isinstance(name, str):
            raise TypeError("Attrib name must be a type str")

        # value can of course be anything (based on self.BASE_MAPS['data_type']

        name, value = self._type_test(self.BASE_MAPS, name, value)

        if name in self.BASE_STATIC_ATTRIBUTES:
            return self._set_static_attribute(attrib, name, value)

        if name in self.BASE_DYNAMIC_ATTRIBUTES:
            return self._set_dynamic_attribute(attrib, name, value)

        # else, we'll assume caller can handle

        return False

    @staticmethod
    def _type_test(maps: dict, name: str, value):
        """
        Do the basic value/type tests
        :param maps:
        :param name:
        :param value:
        :return:
        """

        name = name.lower()

        if name in maps:
            # then it is one of "ours"
            details = maps[name]
            if details['data_type'] is not None:
                check_type = details['data_type']
                if check_type == UserString:
                    # then is the UTF8 type, without EOL
                    value = validate_string(value)

                elif check_type == IndexString:
                    # then is the indexable type, with limited chars
                    value = validate_name(value)

                elif check_type == DataColor:
                    # optional background color (or back/fore ground as tuple)
                    if value == "":
                        value = None

                    if value is not None:
                        try:
                            value = DataColor(value)
                        except ValueError:
                            raise ValueError("{0} is invalid DataTemple['display_color'] attribute")

                elif check_type == Numeric:
                    # then is a float (if INT, make a float)
                    if value is not None:
                        value = Numeric.validate(value)

                elif check_type == Digital:
                    # then is a float (if INT, make a float)
                    if value is not None:
                        value = Digital.validate(value)

                else:
                    if value is not None:
                        if not isinstance(value, check_type):
                            raise TypeError("Base attribute type({0}), expect({1})".format(type(value),
                                                                                           details['data_type']))
                    else:  # value was None
                        if not details['can_clear']:
                            raise ValueError("Attribute({0}) cannot be cleared".format(name))

        return name, value

    def _set_static_attribute(self, attrib, name, value):
        """
        load one base STATIC attribute

        :param name:
        :param value:
        :return: True if attribute handled, else False or exception thrown
        :rtype: bool
        """
        if self._pop_attribute_if_none(attrib, name, value):
            return True

        # these already tested by the base call set_attribute()
        # 'data_name', 'display_name', 'description'

        elif name == 'display_color':
            # optional background color (or back/fore ground as tuple)
            assert isinstance(value, DataColor)

        elif name == 'font_scale':
            value = int(parse_data.parse_integer_or_float(value))
            if value not in self.FONT_SCALE_LIST:
                raise ValueError("Template attribute['font_scale'] {0} is not valid".format(value))

        elif name == 'data_type':
            value = parse_data.clean_string(value).lower()
            if value not in self.DATA_TYPE_LIST:
                raise ValueError("{0} is invalid DataTemple['data_type'] attribute")

            if value == 'digital':
                attrib['value_type'] = bool

            elif value == 'analog':
                attrib['value_type'] = float

            elif value == 'base':
                attrib['value_type'] = None

            elif value == 'string':
                attrib['value_type'] = str

            elif value == 'gps':
                attrib['value_type'] = str

        elif name == 'value_type':
            raise ValueError("set attribute ['data_type'], not 'value_type'")

        elif name == 'failsafe':
            if 'value_type' in attrib:
                value_type = attrib['value_type']
                if value_type is None:
                    # then there is no failsafe allowed!
                    raise ValueError("set attribute ['failsafe'], not allowed")

            else:  # else just accept as submitted
                value_type = None
            value = self._validate_failsafe(value, value_type)

        elif name in ('attach_gps', 'attach_coordinates'):
            value = parse_data.parse_boolean(value)

        # set the actual attribute
        attrib[name] = value

        return True

    def _set_dynamic_attribute(self, attrib, name, value):
        """
        load one base attributes

        :param name:
        :param value:
        :return: True if attribute handled, else False or exception thrown
        :rtype: bool
        """

        if self._pop_attribute_if_none(attrib, name, value):
            return True

        if name == 'source':
            value = data_types.validate_name(value)

        elif name == 'owner_token':
            # any UTF8 string, without EOLN
            value = data_types.validate_string(value)

        # set the actual attribute
        attrib[name] = value

        return True

    def _set_attribute(self, attrib: dict, name: str, value):
        """

        """
        if self._pop_attribute_if_none(attrib, name, value):
            return True

        attrib[name] = value
        return True

    @staticmethod
    def _pop_attribute_if_none(attrib: dict, name: str, value):
        """

        """
        if value is None or value == "":
            # then remove the key from the object
            if name in attrib:
                attrib.pop(name)
            # else it is not there, so no need to delete
            return True
        return False

    @staticmethod
    def _validate_failsafe(value, value_type):
        """
        Given a failsafe, confirm is correct type
        """
        if value_type is not None:
            if value_type == bool:
                value = parse_data.parse_boolean(value)

            elif value_type == int:
                value = parse_data.parse_integer(value)

            elif value_type == float:
                value = parse_data.parse_float(value)

            elif value_type == str:
                value = parse_data.clean_string(str(value))

        # else - TODO - how to test others?
        return value


class StringAttributeHandler(DataAttributeHandler):
    """
    data holding a template (or prototype) data object.

    It includes a converter to 'import' data, possibly modifying it and returning a data_type and uom
    """

    # SUB_ATTRIBUTES = ('uom')

    def __init__(self):
        super().__init__()
        return

    # def set_attribute(self, attrib: dict, name: str, value):
    #     """
    #     Set an attribute
    #     """
    #     name = name.lower()
    #     if super().set_attribute(attrib, name, value):
    #         # then attribute was handled by the base
    #         return True


class BooleanAttributeHandler(DataAttributeHandler):
    """
    A template (or prototype) for a Boolean object.

    ['display_name_true'] = the UTF8 string to show when value is True
    ['display_name_false'] = the UTF8 string to show when value is False
    ['display_color_true'] = the color to show when value is True (like Red or Green)
    ['display_color_false'] = the color to show when value is False (like Red or Green)
    ['invert'] = should value 'set' be inverted?
    ['abnormal_when'] = object is in_alarm, when value == this value
    ['debounce_delay_t_f'] = is the time to delay a change from True to False
    ['debounce_delay_f_t'] = is the time to delay a change from False to True
    ['auto_reset'] = if True, then 'repeated' value are considered changes

    It includes a converter to 'import' data, possibly modifying it and returning a data_type and uom
    """

    SUB_ATTRIBUTES = ('display_name_true', 'display_name_false', 'display_color_true',
                      'display_color_false', 'invert', 'abnormal_when', 'debounce_delay',
                      'auto_reset')

    SUB_MAPS = {
        'display_name_true': {'data_type': UserString},
        'display_name_false': {'data_type': UserString},
        'display_color_true': {'data_type': DataColor},
        'display_color_false': {'data_type': DataColor},
        'invert': {'data_type': Digital},
        'abnormal_when': {'data_type': Digital},
        'auto_reset': {'data_type': Digital},
        'delay_t_f': {'data_type': Numeric},
        'delay_f_t': {'data_type': Numeric},
    }
    # TODO - add when True or False?

    def __init__(self):
        super().__init__()
        return

    def set_attribute(self, attrib: dict, name: str, value):
        """
        Set an attribute

        :return: True if attribute handled, else False or exception thrown
        :rtype: bool
        """
        if super().set_attribute(attrib, name, value):
            # then attribute was handled by the base
            return True

        if name not in self.SUB_ATTRIBUTES:
            raise ValueError("Digital attribute name({0}) is not valid".format(name))

        name, value = self._type_test(self.SUB_MAPS, name, value)

        if name in self.SUB_ATTRIBUTES:
            return self._set_attribute(attrib, name, value)

        # tested in self._type_test() 'display_name_true', 'display_name_false'
        # tested in self._type_test() 'display_color_true', 'display_color_false'
        # tested in self._type_test() 'invert', 'abnormal_when', 'auto_reset'
        # tested in self._type_test() 'delay_t_f'
        # tested in self._type_test() 'delay_f_t'

        return False


class NumericAttributeHandler(DataAttributeHandler):
    """
    data holding a template (or prototype) data object.

    It includes a converter to 'import' data, possibly modifying it and returning a data_type and uom
    """

    DEF_PRECISION = 0.0001

    SUB_ATTRIBUTES = ('uom')
    # TODO - track stats for min/max/avg?

    SUB_MAPS = {
        'uom': {'data_type': UserString},
    }

    def __init__(self):
        super().__init__()
        return

    def set_attribute(self, attrib: dict, name: str, value):
        """
        Set an attribute

        :return: True if attribute handled, else False or exception thrown
        :rtype: bool

        """
        name = name.lower()
        if super().set_attribute(attrib, name, value):
            # then attribute was handled by the base
            return True

        return False


class GpsAttributeHandler(DataAttributeHandler):
    """
    data holding a template (or prototype) data object.

    It includes a converter to 'import' data, possibly modifying it and returning a data_type and uom
    """

    SUB_ATTRIBUTES = ('gps_mode', 'latitude', 'longitude', 'latitude_filter', 'longitude_filter',
                      'ground_speed_filter', 'is_move_cutoff')

    SUB_MAPS = {
        'gps_mode': {'data_type': UserString},
        'latitude': {'data_type': Numeric},
        'longitude': {'data_type': Numeric},
        'latitude_filter': {'data_type': Numeric},
        'longitude_filter': {'data_type': Numeric},
        'ground_speed_filter': {'data_type': Numeric},
        'is_move_cutoff': {'data_type': Numeric},
    }

    def __init__(self):
        super().__init__()
        return

    def set_attribute(self, attrib: dict, name: str, value):
        """
        Set an attribute
        """
        if super().set_attribute(attrib, name, value):
            # then attribute was handled by the base
            return True

        if name not in self.SUB_ATTRIBUTES:
            raise ValueError("GPS attribute name({0}) is not valid".format(name))

        name, value = self._type_test(self.SUB_MAPS, name, value)

        if name in self.SUB_ATTRIBUTES:
            return self._set_attribute(attrib, name, value)

        return False
