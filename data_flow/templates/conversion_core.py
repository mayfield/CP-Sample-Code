# File: conversion_core.py
# Desc: the base class for conversion filters

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#


class ConversionCore(object):
    """
    A 'conversion' is a process filter, which possibly converts an input into a specific output;

    Examples:
    - accept a temperature as either DegF or DegC, but make sure output is DegF
    - discard null data, as for example a room is almost never 0.00000 DegF
    """

    def __init__(self, name=None, param=None):
        if name is None:
            name = "core"
        self.name = name
        return

    @staticmethod
    def code_name():
        return 'ConversionCore'

    @staticmethod
    def code_version():
        return __version__

    def convert(self, value, param=None):
        raise NotImplementedError


class ConversionNonNull(ConversionCore):
    """
    Discard null data, as for example a room is almost never 0.00000 DegF. Assuming we get a new value fequently
    then a true 0.0000 discarded will be replaced by a 0.0023 or other near-zero value.
    """
    def __init__(self, name=None):
        if name is None:
            name = "nonNull"
        ConversionCore.__init__(self, name)
        return

    @staticmethod
    def code_name():
        return 'ConversionNonNull'

    def convert(self, value, param=None):
        """
        Prevent propagating a true null sample. For example, a real temperature is not likely 0.00000 DegC

        :param value:
        :param param:
        :return:
        """
        if value in (None, 0, 0.0, ""):
            return None
        return value
