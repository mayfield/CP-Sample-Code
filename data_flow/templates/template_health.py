# File: template_health.py
# Desc: template for data as a health 0.0% to 100%

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Aug Lynn
#       * initial draft
#

from data.data_template import NumTemplate
from data.data_color import DataColor


def create_health_data_object(path, name=None):
    """
    Create and initialize a numeric data object handling 0-100% health

    :param path: the element path to use
    :type path: str
    :param name: the proposed name, if None then set to "health"
    :type name" str or None
    :rtype: TemplateHealth
    """
    from data.data_object import NumericObject
    from data.data_base import fetch_template_by_name

    if name is None:
        name = "health"

    if path is None or not isinstance(path, str):
        raise ValueError("Data Object PATH must be type()=str")

    # then create the health data object
    data = NumericObject(name)
    data.set_attribute('path', path)
    data.set_template(fetch_template_by_name(name))
    # self.database.add_to_data_base(data)
    return data


class TemplateHealth(NumTemplate):
    """
    Template for data holding a 0-100% health value
    """

    LOW_BAND_TOP = 75.0
    MID_BAND_TOP = 98.0
    # HI_BAND = 100.0

    LOW_BAND_CHANGE = 5.0
    MID_BAND_CHANGE = 1.0
    HI_BAND_CHANGE = 0.1

    # DataColor = (back, fore)
    LOW_BAND_COLOR = ('red', 'gold')
    MID_BAND_COLOR = ('yellow', 'black')
    HI_BAND_COLOR = ('white', 'black')

    LOW_BAND_NAME = 'error'
    MID_BAND_NAME = 'warn'
    HI_BAND_NAME = 'good'

    def __init__(self, name=None):

        if name is None:
            name = '_health'

        super().__init__(name)

        self.low_color = DataColor(self.LOW_BAND_COLOR)
        self.mid_color = DataColor(self.MID_BAND_COLOR)
        self.hi_color = DataColor(self.HI_BAND_COLOR)

        self.set_attribute('uom', '%')

        return

    @staticmethod
    def code_name():
        return 'TemplateHealth'

    @staticmethod
    def code_version():
        return __version__

    def process_value(self, value, param=None):
        """Given a new value, convert and process returning details"""
        if isinstance(value, int):
            value = float(value)

        elif not isinstance(value, float) or not(0.0 <= value <= 100.0):
            raise ValueError("Health Data Value can only be 0.0 to 100.0")

        value, quality_change = super().process_value(value, param)

        return value, quality_change

    def test_if_changed(self, old_value, new_value):

        assert isinstance(old_value, float)
        assert 0.0 <= new_value <= 100.0
        assert isinstance(new_value, float)
        assert 0.0 <= old_value <= 100.0

        if old_value == new_value:
            # then was no change
            return False, old_value

        change_value = abs(old_value - new_value)

        if old_value > self.MID_BAND_TOP:
            # then 98.0 < old_value <= 100.0
            if (new_value < self.MID_BAND_TOP) or (change_value >= self.HI_BAND_CHANGE):
                # if new value changed bands then assume is change, else compare to change limit
                return True, new_value

        elif old_value > self.LOW_BAND_TOP:
            # then 75.0 <= old_value <= 98.0
            if not (self.LOW_BAND_TOP < new_value <= self.MID_BAND_TOP) and \
                    (change_value >= self.MID_BAND_CHANGE):
                # if new value changed bands then assume is change, else compare to change limit
                return True, new_value

        else:  # then 0.0 <= old_value < 75.0
            if change_value >= self.LOW_BAND_CHANGE:
                return True, new_value

        # else, value did not change enough
        return False, old_value

    def update_band_details(self, value):
        """
        Given 'current' value, define the band name and colors
        """
        assert 0<= value <= 100.0

        if value <= self.LOW_BAND_TOP:
            return self.LOW_BAND_NAME, self.low_color

        if value <= self.MID_BAND_TOP:
            return self.MID_BAND_NAME, self.mid_color

        return self.HI_BAND_NAME, self.hi_color
