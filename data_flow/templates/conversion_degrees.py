# File: conversion_degrees.py
# Desc: the conversion filters for degree F or C

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#
from data.templates.conversion_core import ConversionCore


class ConversionDegF(ConversionCore):
    """
    attempt to force a temperature to always be Deg F (so 'pass' DegF but convert DegC)
    """

    def __init__(self, name=None):
        if name is None:
            name = "degF"
        super().__init__(name)
        return

    @staticmethod
    def code_name():
        return 'ConversionDegF'

    def convert(self, value, param=None):
        """
        if PARAM implies is Celsius, then convert to Fahrenheit.

        :param value: the value to test for conversion
        :type value: float
        :param param: the unit-of-measure of the input value
        :rtype: float
        """
        if param is not None:
            param = param.lower()
            if param in ('c', 'degc', 'degreec', 'degree_c', 'celsius'):
                # then we want to convert
                value = (value * 1.8) + 32.0

        return value, 0


class ConversionDegC(ConversionCore):
    """
    attempt to force a temperature to always be Deg C (so 'pass' DegC but convert DegF)
    """

    def __init__(self, name=None):
        if name is None:
            name = "degC"
        super().__init__(name)
        return

    @staticmethod
    def code_name():
        return 'ConversionDegC'

    def convert(self, value, param=None):
        """
        if PARAM implies is Fahrenheit, then convert to Celsius.

        :param value: the value to test for conversion
        :type value: float
        :param param: the unit-of-measure of the input value
        :rtype: float
        """
        if param is not None:
            param = param.lower()
            if param in ('f', 'degf', 'degreef', 'degree_f', 'fahrenheit'):
                # then we want to convert
                value = ((value - 32) * 5.0) / 9.0

        return value, 0
