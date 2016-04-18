# File: conversion_clamps.py
# Desc: the conversion filters to limit values range

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#
from data.templates.conversion_core import ConversionCore
from common.quality import QUALITY_MASK_CLAMP_LOW, QUALITY_MASK_CLAMP_HIGH, QUALITY_MASK_UNDER_RANGE, \
    QUALITY_MASK_OVER_RANGE
from common.parse_data import parse_integer_or_float, parse_boolean


class ConversionClamp(ConversionCore):
    """
    A Low-Clamp conversion acts as a lower limit. A simple example is a value which can only physically be
    0 to 100%, so values like -0.7% is not possible.
    """

    def __init__(self, name=None, param=None):
        if name is None:
            name = "Clamp"
        super().__init__(name)

        # confirm is int or float, convert from string if required, throw exceptions if wrong type
        self._output = self.set_clamp_value(param)

        # by default, tag with over/under only. Not the range error.
        self._range_fault = self.set_range_fault(False)

        # by default, the fancier band clamping is disabled
        self._upper = None
        self._lower = None

        return

    def set_clamp_value(self, value):
        """
        Change or set the clamp value, which can be int or float

        :param value: the proposed value for the clamp
        :type value: int, float, string
        :return: the actual value set. Exception is thrown if not valid
        :rtype: int or float
        """
        self._output = parse_integer_or_float(value)
        return self._output

    def set_upper_value(self, value):
        """
        Change or set the clamp value, which can be int or float

        :param value: the proposed value for the clamp
        :type value: int, float, string
        :return: the actual value set. Exception is thrown if not valid
        :rtype: int or float
        """
        self._upper = parse_integer_or_float(value)
        return self._upper

    def set_lower_value(self, value):
        """
        Change or set the clamp value, which can be int or float

        :param value: the proposed value for the clamp
        :type value: int, float, string
        :return: the actual value set. Exception is thrown if not valid
        :rtype: int or float
        """
        self._lower = parse_integer_or_float(value)
        return self._lower

    def set_range_fault(self, value):
        """
        Change or set the clamp value

        :return:
        """
        self._range_fault = parse_boolean(value)
        return self._range_fault

    def convert(self, value, param=None):
        raise NotImplementedError


class ConversionClampLow(ConversionClamp):
    """
    A Low-Clamp conversion acts as a lower limit. A simple example is a value which can only physically be
    0 to 100%, so values like -0.7% is not possible.
    """

    def __init__(self, name=None, param=None):
        if name is None:
            name = "lowClamp"
        super().__init__(name, param)
        return

    @staticmethod
    def code_name():
        return 'ConversionClampLow'

    def convert(self, value, param=None):
        """
        test if value is below our minimum clamp.

        Mode #1: if _output < value < _upper, then set to _output, but quality is zero/unaffected
        Mode #2: if value < _output, _lower is None, then set to _output, and return quality as QUALITY_MASK_CLAMP_LOW
        Mode #3: if _lower < value < _output, then set to _output, and return quality as QUALITY_MASK_CLAMP_LOW
        Mode #4: if value < _lower, then leave value unchanged, but set QUALITY_MASK_UNDER_RANGE

        :param value: the value to test for conversion
        :type value: float or int
        :rtype: float, int
        """
        assert self._output is not None

        quality_change = 0
        if self._upper is not None and (self._output <= value < self._upper):
            # then mode #1 is true, no change to quality_change
            value = self._output

        elif value < self._output:
            # then mode #2, #3, or #4 might be true
            if self._lower is None:
                # then node #2 is True
                value = self._output
                quality_change = QUALITY_MASK_CLAMP_LOW

            else:  # lower is a value
                if self._lower <= value < self._output:
                    # then mode #3 is true, quality_change
                    value = self._output
                    quality_change = QUALITY_MASK_CLAMP_LOW

                elif value < self._lower:
                    # then mode #4 is true, no change to value, so no Clamp error, but RANGE error
                    quality_change = QUALITY_MASK_UNDER_RANGE

        # else, value is large enough

        if self._range_fault and quality_change:
            # then include tha hardware fault values
            quality_change |= QUALITY_MASK_UNDER_RANGE

        return value, quality_change


class ConversionClampHigh(ConversionClamp):
    """
    A High-Clamp conversion acts as a upper limit. A simple example is a value which can only physically be
    0 to 100%, so values like 102% is not possible.
    """

    def __init__(self, name=None, param=None):
        if name is None:
            name = "clampHigh"
        super().__init__(name, param)
        return

    @staticmethod
    def code_name():
        return 'ConversionClampHigh'

    def convert(self, value, param=None):
        """
        test if value is above our maximum clamp.

        Mode #1: if _lower < value < _output, then set to _output, but quality is zero/unaffected
        Mode #2: if value < _output, _upper is None, then set to _output, and return quality as QUALITY_MASK_CLAMP_HI
        Mode #3: if _output < value < _upper, then set to _output, and return quality as QUALITY_MASK_CLAMP_HI
        Mode #4: if value > _upper, then leave value unchanged, but set QUALITY_MASK_OVER_RANGE

        :param value: the value to test for conversion
        :type value: float or int
        :rtype: float, int
        """
        assert self._output is not None

        quality_change = 0
        if self._lower is not None and (self._lower < value <= self._output):
            # then mode #1 is true, no change to quality_change
            value = self._output

        elif self._output < value:
            # then mode #2, #3, or #4 might be true
            if self._upper is None:
                # then node #2 is True
                value = self._output
                quality_change = QUALITY_MASK_CLAMP_HIGH

            else:  # upper is value
                if self._output < value <= self._upper:
                    # then mode #3 is true, quality_change
                    value = self._output
                    quality_change = QUALITY_MASK_CLAMP_HIGH

                elif self._upper < value:
                    # then mode #4 is true, no change to value, so no Clamp error, but RANGE error
                    quality_change = QUALITY_MASK_OVER_RANGE

        # else, value is large enough

        if self._range_fault and quality_change:
            # then include tha hardware fault values
            quality_change |= QUALITY_MASK_OVER_RANGE

        return value, quality_change
