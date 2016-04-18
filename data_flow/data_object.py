# File: morsel_object.py
# Desc: a morsel which holds data - an end-point

from data.data_core import DataCore
from data.data_types import data_type_python_to_internal, data_type_export_to_json, validate_string
from data.data_sample import DataSample

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
# 1.1.0: 2015-Aug Lynn
#       * add the sub-types
#


class DataObject(DataCore):
    """
    The base data objects
    """

    _BASE_ATTRIBUTE_HANDLER = None

    def __init__(self, name):

        super().__init__(name)

        self['class'] = self.code_name()
        self._attrib['role'] = "data"

        if self._BASE_ATTRIBUTE_HANDLER is None:
            from data.data_attribute import DataAttributeHandler
            DataObject._BASE_ATTRIBUTE_HANDLER = DataAttributeHandler()

        # DATA_TYPE_LIST = ('base', 'string', 'digital', 'gps', 'analog')
        self._BASE_ATTRIBUTE_HANDLER.set_attribute(self._attrib, 'data_type', 'base')
        return

    @staticmethod
    def code_name():
        return 'DataObject'

    @staticmethod
    def code_version():
        return __version__

    def set_parent(self, parent):
        if not parent['class'] in ('DataCore', 'DataObject'):
            raise TypeError("Parent cannot be class %s" % parent['class'])
        self._parent = parent

    def set_attribute(self, name: str, value):
        """
        Set an attribute
        """
        return self._BASE_ATTRIBUTE_HANDLER.set_attribute(self._attrib, name, value)

    def set_attribute_string(self, key, value):
        """
        Get a under description, which is any unicode (per our restrictions)

        :param key: the self._attrib() key to set
        :type key: str
        :param value: the proposed string
        :type value: str or unicode or None
        :return: the attrib is returned if set, else an exception will be thrown
        :rtype: unicode
        """
        value = validate_string(value)
        return self.set_attribute(key, value)

    @staticmethod
    def validate_data_type(value):
        """
        :param value: Morsel data type
        :type value: types.TypeType
        :return:
        """
        return data_type_python_to_internal(value)

    def get_json_data_type(self, value=None):
        """
        :param value: Morsel data type
        :type value: types.TypeType
        :return:
        """
        if value is None:
            # if None, then use our OWN type
            value = self['data_type']

        return data_type_export_to_json(value)

    def set_value(self, value, now=None, param=None):
        """
        Set a value - we need to isolate self.__value, as we need the template to filter the setting.

        :param value: the proposed value
        :param now: the time to use in the sample (if None, use time.time())
        :type now: float or None
        :return: T if the value changed, else F if no change, else exception will be thrown
        :rtype: bool
        """
        work = self._attrib.get('value', None)
        if work is None:
            # then no data sample, so create one
            work = DataSample()
            # copy our template to it
            work.set_template(self._template)

        if not isinstance(work, DataObject):
            raise TypeError("DataObject() is not DataSample")

        work.set_value(value, now, param)
        self['value'] = work
        return True


class StringObject(DataObject):

    _SUB_ATTRIBUTE_HANDLER = None

    def __init__(self, name):
        super().__init__(name)
        self['class'] = self.code_name()

        if self._SUB_ATTRIBUTE_HANDLER is None:
            from data.data_attribute import StringAttributeHandler
            StringObject._SUB_ATTRIBUTE_HANDLER = StringAttributeHandler()

        self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, 'data_type', 'string')
        return

    @staticmethod
    def code_name():
        return 'StringObject'

    def set_attribute(self, name: str, value):
        """
        Set an attribute
        """
        return self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, name, value)


class BooleanObject(DataObject):

    _SUB_ATTRIBUTE_HANDLER = None

    def __init__(self, name):
        super().__init__(name)
        self['class'] = self.code_name()

        if self._SUB_ATTRIBUTE_HANDLER is None:
            from data.data_attribute import BooleanAttributeHandler
            BooleanObject._SUB_ATTRIBUTE_HANDLER = BooleanAttributeHandler()

        self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, 'data_type', 'digital')
        return

    @staticmethod
    def code_name():
        return 'BooleanObject'

    def set_attribute(self, name: str, value):
        """
        Set an attribute
        """
        return self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, name, value)


class NumericObject(DataObject):

    _SUB_ATTRIBUTE_HANDLER = None

    def __init__(self, name):
        super().__init__(name)
        self['class'] = self.code_name()

        if self._SUB_ATTRIBUTE_HANDLER is None:
            from data.data_attribute import NumericAttributeHandler
            NumericObject._SUB_ATTRIBUTE_HANDLER = NumericAttributeHandler()

        self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, 'data_type', 'analog')
        return

    @staticmethod
    def code_name():
        return 'NumericObject'

    def set_attribute(self, name: str, value):
        """
        Set an attribute
        """
        return self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, name, value)


class GpsObject(DataObject):

    _SUB_ATTRIBUTE_HANDLER = None

    def __init__(self, name):
        super().__init__(name)
        self['class'] = self.code_name()

        if self._SUB_ATTRIBUTE_HANDLER is None:
            from data.data_attribute import GpsAttributeHandler
            GpsObject._SUB_ATTRIBUTE_HANDLER = GpsAttributeHandler()

        self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, 'data_type', 'gps')
        return

    @staticmethod
    def code_name():
        return 'GpsObject'

    def set_attribute(self, name: str, value):
        """
        Set an attribute
        """
        return self._SUB_ATTRIBUTE_HANDLER.set_attribute(self._attrib, name, value)


def create_data_object(name: str, obj_type: str):
    """
    Create a DataObject
    :return:
    :rtype: DataObject
    """
    # technically, the types are listed in DataAttributeHandler.DATA_TYPE_LIST
    obj_type = obj_type.lower()

    if obj_type == 'base':
        return DataObject(name)

    elif obj_type == 'string':
        return StringObject(name)

    elif obj_type == 'digital':
        return BooleanObject(name)

    elif obj_type == 'analog':
        return NumericObject(name)

    elif obj_type == 'gps':
        return GpsObject(name)

    raise ValueError("data object type({0} is not valid".format(obj_type))

