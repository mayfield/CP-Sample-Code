# File: morsel_object.py
# Desc: a morsel which holds data - an end-point

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

from data.data_core import DataCore


class DataAlarm(DataCore):
    """
    A data alarm is attached to one of more data objects, which it evaluates as each new value is set.

    TODO: should 1 alarm be shared by many objects? For example, if we have 10 similar tanks, does it make sense to
    have all 10 use the same low alarm? Maybe not - perhaps we have 10 alarms, but allow them to point to a common
    'setting', which allows all 10 to share an alarm level (like 5%) and changing 1 setting affects all 10.

    As mentioned elsewhere, in this shared scenario, perhaps one tank can 'split off' from the group and have a
    unique alarm level setting.
    """

    def __init__(self, name):

        super(DataAlarm, self).__init__(name)
        # self['role'] = self.ROLE_ALARM
        return

    @staticmethod
    def code_name():
        return 'DataAlarm'

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

        # ['last_value'] ['uom'] ["name"] handled by DataBase
        return super(DataAlarm, self).export_json(result)

    def import_json(self, source, strict=True):
        """
        rebuild self from a JSON string

        :param source: the JSON source
        :return:
        :rtype: dict
        """
        # validate and convert to python DICT
        # ["name"] handled by DataBase
        result = super(DataAlarm, self).import_json(source, strict)
        # result["role"] = self.ROLE_OBJECT
        return True
