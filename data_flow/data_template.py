# File: data_template.py
# Desc: data holding a template (or prototype) data object

__version__ = "1.1.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
# 1.1.0: 2015-Aug Lynn
#       *
#

import copy

import data.data_types as data_types
from data.data_core import DataCore
from data.data_sample import DataSample
from data.data_color import DataColor
from common.quality import QUALITY_MASK_CLAMP_LOW, QUALITY_MASK_CLAMP_HIGH
from common.data_precision import validate_precision_value, get_precision_string_format, use_precision_to_reduce_value
import common.parse_data as parse_data
from common.parse_duration import TimeDuration


class DataTemplate(DataCore):
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

    It includes a converter to 'import' data, possibly modifying it and returning data_type and uom
    """

    BASE_ATTRIBUTES = ('data_name', 'display_name', 'display_color', 'font_scale', 'data_type',
                       'description', 'value_type', 'failsafe', 'attach_gps')

    DATA_TYPE_LIST = ('base', 'string', 'digital', 'gps', 'analog')

    FONT_SCALE_LIST = (50, 75, 100, 125, 150)

    def __init__(self, name):

        # DataObject.__init__(self, name)
        super().__init__(name)
        self['class'] = 'DataTemplate'
        self['role'] = 'template'

        self._value = None

        self._conversions = []
        return

    @staticmethod
    def code_name():
        return 'DataTemplate'

    @staticmethod
    def code_version():
        return __version__

    def set_attribute(self, name: str, value):
        """
        load one of the Template attributes

        :param name:
        :param value:
        :return:
        """
        name = name.lower()
        if name not in self.BASE_ATTRIBUTES:
            raise ValueError("Template attribute name({0}) is not valid".format(name))

        if name == 'data_name':
            value = data_types.validate_name(value)

        elif name in ('display_name', 'description'):
            # any UTF8 string, without EOLN
            value = data_types.validate_string(value)

        elif name == 'display_color':
            try:
                value = DataColor(value)
            except ValueError:
                raise ValueError("{0} is invalid DataTemple['display_color'] attribute")

        elif name == 'font_scale':
            value = int(parse_data.parse_integer_or_float(value))
            if value not in self.FONT_SCALE_LIST:
                raise ValueError("Template attribute['font_scale'] {0} is not valid".format(value))

        elif name == 'data_type':
            value = parse_data.clean_string(value).lower()
            if value not in self.DATA_TYPE_LIST:
                raise ValueError("{0} is invalid DataTemple['data_type'] attribute")

            if value == 'digital':
                self['value_type'] = bool

            elif value == 'analog':
                self['value_type'] = float

            elif value == 'base':
                self['value_type'] = None

            elif value == 'string':
                self['value_type'] = str

            elif value == 'gps':
                self['value_type'] = str

        elif name == 'value_type':
            pass

        elif name == 'failsafe':
            value = self._validate_failsafe(value)

        elif name == 'attach_gps':
            value = parse_data.parse_boolean(value)

        # set the actual attribute
        self[name] = value
        return

    def add_conversion(self, convert):
        """
        Add an item to the conversion list

        :param convert: what to add to the list
        :type convert: ConversionCore
        :rtype: None
        """
        from data.templates.conversion_core import ConversionCore

        if not isinstance(convert, ConversionCore):
            raise TypeError("Cannot add conversion of type:%s" % type(convert))

        self._conversions.append(convert)
        return

    def remove_conversion(self, code_name):
        """
        Remove an item to the conversion list. use the 'code_name' as trying to match complex class
        types fails or succeeds based on HOW the class was imported! code_name() is consistent.

        :param code_name: the 'code_name' of the conversion to remove
        :type code_name: ConversionCore
        :return: the number of conversions deleted
        :rtype: int
        """
        if not isinstance(code_name, str):
            raise TypeError("Cannot remove conversion with name of type:%s" % type(code_name))

        new_list = []
        remove_count = 0
        for convert in self._conversions:
            if convert.code_name() != code_name:
                new_list.append(convert)
            else:
                remove_count += 1

        self._conversions = new_list
        return remove_count

    def get_uom(self):
        return None

    def get_string(self, data):
        """
        Given one of our DataSample, format it as a string. For temperature, we reduce to
        units (int) and attach the UOM (F or C)

        :param data:
        :type data: DataSample
        :return:
        :rtype: str
        """
        return str(data.get_value())

    def process_value(self, value, param=None):
        """
        Given one of our DataSample, format it as a string

        process_value(value)

        :param value:
        :param param: an option
        :return:
        :rtype: value, int
        """
        quality_change = 0
        if len(self._conversions) > 0:

            for conversion in self._conversions:
                value_result, quality_result = conversion.convert(value, param)

                if quality_result:
                    quality_change |= quality_result

                if value_result is None:
                    return None, quality_change
                value = value_result

        return value, quality_change

    def test_if_changed(self, old_value, new_value):
        """
        Test if the value has changed, which by default is ANY AMOUNT
        """
        if old_value == new_value:
            return False, old_value
        else:
            return True, new_value

    def _validate_failsafe(self, value, value_type=None):
        """
        Given a failsafe, confirm is correct type
        """
        if value_type is None:
            if 'value_type' not in self._attrib:
                raise ValueError("Must set ['value_type'] first")
            value_type = self['value_type']

        if value_type == bool:
            value = parse_data.parse_boolean(value)

        elif value_type == int:
            value = parse_data.parse_integer(value)

        elif value_type == float:
            value = parse_data.parse_float(value)

        elif value_type == str:
            value = parse_data.clean_string(value)

        # else - TODO - how to test others?
        return value


class BoolTemplate(DataTemplate):
    """
    A template (or prototype) for a Boolean object.

    ['display_name_true'] = the UTF8 string to show when value is True
    ['display_name_false'] = the UTF8 string to show when value is False
    ['display_color_true'] = the color to show when value is True (like Red or Green)
    ['display_color_false'] = the color to show when value is False (like Red or Green)
    ['invert'] = should value 'set' be inverted?
    ['abnormal_when'] = object is in_alarm, when value == this value
    ['debounce_delay'] = is the time to delay a change
    ['auto_reset'] = if True, then 'repeated' value are considered changes

    It includes a converter to 'import' data, possibly modifying it and returning data_type and uom
    """

    DIGITAL_ATTRIBUTES = ('display_name_true', 'display_name_false',
                          'display_color_true', 'display_color_false',
                          'invert', 'abnormal_when', 'debounce_delay', 'auto_reset')

    def __init__(self, name):
        super().__init__(name)
        self['class'] = 'BoolTemplate'
        return

    def set_attribute(self, name: str, value):
        """
        load one of the Template attributes

        :param name:
        :param value:
        :return:
        """
        name = name.lower()
        if name in self.BASE_ATTRIBUTES:
            return DataTemplate.set_attribute(self, name, value)

        if name not in self.DIGITAL_ATTRIBUTES:
            raise ValueError("Digital Template attribute name({0}) is not valid".format(name))

        try:
            if name in ('display_name_true', 'display_name_false'):
                # any UTF8 string, without EOLN
                value = data_types.validate_string(value)

            elif name in ('display_color_true', 'display_color_false'):
                value = DataColor(value)

            elif name in ('invert', 'abnormal_when', 'auto_reset'):
                value = parse_data.parse_boolean(value)

            elif name == 'debounce_delay':
                value = TimeDuration(value)

        except:
            raise ValueError("{0} is invalid DataTemple['{1}'] attribute".format(value, name))

        # set the actual attribute
        self[name] = value
        return True

    def get_uom(self):
        """
        return a UOM / Unit of Measure - if any
        :return: str or None
        """
        if self._value is None:  # value hasn't been set yet, return None
            return None

        if self._value:  # then is TRUE, so return the TRUE display tag
            return self._attrib.get('display_name_true', None)

        else:  # is FALSE, so return the FALSE display tag
            return self._attrib.get('display_name_false', None)

    def get_string(self, data):
        """
        Given one of our DataSample, format it as a string. For temperature, we reduce to
        units (int) and attach the UOM (F or C)

        :param data:
        :type data: DataSample
        :return:
        :rtype: str
        """
        value = data.get_value()
        if not isinstance(value, bool):
            raise ValueError("sample is not Digital:{0}".format(data))

        if value:
            if 'display_name_true' in self._attrib:
                # then we have a display name
                return 'True({0})'.format(self['display_name_true'])

        else:  # is false
            if 'display_name_false' in self._attrib:
                # then we have a display name
                return 'False({0})'.format(self['display_name_false'])

        return str(value)

    def process_value(self, value, param=None):
        """
        Given one of our DataSample, format it as a string

        process_value(value)

        :param value:
        :param param: an option
        :return:
        :rtype: value, int
        """

        # clean up the boolean
        value = parse_data.parse_boolean(value)

        # first, have base do any stock conversions
        value, quality_change = super().process_value(value, param)

        if self._attrib.get('invert', False):
            value = not value

        # 'abnormal_when', 'debounce_delay', 'auto_reset'

        return value, quality_change

    # use super() test_if_changed(self, old_value, new_value):


class NumTemplate(DataTemplate):
    """
    data holding a template (or prototype) data object.

    It includes a converter to 'import' data, possibly modifying it and returning data_type and uom
    """

    DEF_PRECISION = 0.0001

    ANALOG_ATTRIBUTES = ('uom')

    def __init__(self, name):

        # DataObject.__init__(self, name)
        super().__init__(name)
        self['class'] = 'NumTemplate'
        self['precision'] = self.DEF_PRECISION

        return

    @staticmethod
    def code_name():
        return 'DataTemplate'

    @staticmethod
    def code_version():
        return __version__

    def set_precision(self, value):
        """
        Set the format and rounding precision

        :param value:
        :type value: float
        :return:
        """
        if not validate_precision_value(value):
            raise ValueError("set_precision(%s) is not a valid precision input", value)

        self['precision'] = value
        return

    def get_uom(self):
        """
        return a UOM / Unit of Measure - if any
        :return: str or None
        """
        return self._attrib.get('uom', None)

    def get_string(self, data):
        """
        Given one of our DataSample, format it as a string. For temperature, we reduce to
        units (int) and attach the UOM (F or C)

        :param data:
        :type data: DataSample
        :return:
        :rtype: str
        """
        value = data.get_value()
        if isinstance(value, float):
            value = use_precision_to_reduce_value(self['precision'], value)
            form = get_precision_string_format(self['precision'])
            value = form % value

        else:
            value = str(value)

        uom = self['uom']
        if uom is not None and uom != "":
            value += " " + uom

        return value

    def set_attribute(self, name: str, value):
        """
        load one of the Template attributes

        :param name:
        :param value:
        :return:
        """
        name = name.lower()
        if name in self.BASE_ATTRIBUTES:
            return DataTemplate.set_attribute(self, name, value)

        if name not in self.ANALOG_ATTRIBUTES:
            raise ValueError("Analog Template attribute name({0}) is not valid".format(name))

        # try:
        #     if name in ('display_name_true', 'display_name_false'):
        #         # any UTF8 string, without EOLN
        #         value = data_types.validate_string(value)
        #
        #     elif name in ('display_color_true', 'display_color_false'):
        #         value = DataColor(value)
        #
        #     elif name in ('invert', 'abnormal_when', 'auto_reset'):
        #         value = parse_data.parse_boolean(value)
        #
        #     elif name == 'debounce_delay':
        #         value = TimeDuration(value)
        #
        # except:
        #     raise ValueError("{0} is invalid DataTemple['{1}'] attribute".format(value, name))

        # set the actual attribute
        self[name] = value
        return True

    def process_value(self, value, param=None):
        """
        Given one of our DataSample, format it as a string

        process_value(value)

        :param value:
        :param param: an option
        :return:
        :rtype: value, int
        """
        quality_change = 0
        if len(self._conversions) > 0:

            for conversion in self._conversions:
                value_result, quality_result = conversion.convert(value, param)

                if quality_result:
                    quality_change |= quality_result

                if value_result is None:
                    return None, quality_change
                value = value_result

        # check if we have min/max values
        if 'min_value' in self._attrib:
            if value < self['min_value']:
                value = self['min_value']
                quality_change |= QUALITY_MASK_CLAMP_LOW

        if 'max_value' in self._attrib:
            if value > self['max_value']:
                value = self['max_value']
                quality_change |= QUALITY_MASK_CLAMP_HIGH

        value = use_precision_to_reduce_value(self['precision'], value)

        return value, quality_change


def create_data_template(name):
    """
    Create a DataObject
    :return:
    :rtype: DataObject
    """
    value = DataTemplate(name)
    return value
