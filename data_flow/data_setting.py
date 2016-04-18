# File: data_setting.py
# Desc: a morsel which holds a setting

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#

"""
a morsel which holds data - an end-point
"""
import copy

from data.data_object import DataObject


class DataSetting(DataObject):

    def __init__(self, name):

        super(DataSetting, self).__init__(name)
        self['class'] = self.code_name()
        self['role'] = 'setting'

        return

    @staticmethod
    def code_name():
        return 'DataSetting'

    @staticmethod
    def code_version():
        return __version__

    def export_json(self, pass_in=None):
        """
        Dump self as a JSON string

        :return:
        :rtype: str
        """
        if pass_in is None:
            result = dict()
        else:
            result = copy.copy(pass_in)

        result['class'] = self.code_name()

        return super(DataSetting, self).export_json(result)

    def import_json(self, source, strict=True):
        """
        rebuild self from a JSON string

        :param source: the JSON source
        :return:
        :rtype: dict
        """
        # validate and convert to python DICT
        # ["name"] handled by DataBase
        result = super(DataSetting, self).import_json(source, strict)
        result["class"] = self.code_name()
        return True


def create_data_setting(name):
    """
    Create a DataObject
    :return:
    :rtype: DataObject
    """
    value = DataSetting(name)
    return value
