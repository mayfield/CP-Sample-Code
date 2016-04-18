# File: template_date_time.py
# Desc: template for data which is a date+time, or just time

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Aug Lynn
#       * initial draft
#
#
from data.data_template import DataTemplate
import time


class TemplateDateTime(DataTemplate):
    """
    Template for data with date as ISO STRING, such as:
    - ISO = "2015-08-18T18:46:23Z"
    - SEC = "2015-08-18 18:46:23"
    - HRS = "2015-08-18 18:46"
    """

    # values for self._mode
    MODE_ISO = 'iso'
    MODE_SEC = 'sec'
    MODE_HRS = 'hrs'
    MODE_DEFAULT = MODE_ISO

    def __init__(self, name=None):

        if name is None:
            name = 'datetime'

        super().__init__(name)

        self._mode = self.MODE_DEFAULT

        return

    @staticmethod
    def code_name():
        return 'TemplateDateTime'

    @staticmethod
    def code_version():
        return __version__

    def process_value(self, value, param=None):
        """Given a new value, convert and process returning details"""
        if isinstance(value, int):
            value = float(value)

        elif isinstance(value, str):
            return value

        elif not isinstance(value, float):
            raise ValueError("Health Data Value can only be 0.0 to 100.0")

        # Is there any reason to use 'conversions' on value?
        # value, quality_change = super().process_value(value, param)
        quality_change = 0

        if self._mode == self.MODE_ISO:
            # then string like "2015-08-18T18:46:23Z"
            value = time.strftime("Y-m-dZH:M:SZ", time.gmtime(value))

        elif self._mode == self.MODE_SEC:
            # then string like "2015-08-18 18:46:23"
            value = time.strftime("Y-m-d H:M:S", time.gmtime(value))

        else:
            assert self._mode == self.MODE_HRS
            # then string like "2015-08-18 18:46"
            value = time.strftime("Y-m-d H:M", time.gmtime(value))

        return value, quality_change
