# File: template_temperature.py
# Desc: template for data as temperature

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#
from data.data_template import NumTemplate
from data.templates.conversion_degrees import ConversionDegF, ConversionDegC


class TemplateTemperature(NumTemplate):
    """
    data holding a template (or prototype) data object.

    It includes a converter to 'import' data, possibly modifying it and returning a data_type and uom
    """

    DEF_DEGF = True

    def __init__(self, name=None):

        if name is None:
            name = 'temperature'

        super().__init__(name)

        # we want to round down to units, like 72
        self.set_precision(1.0)

        # set the ['degf'] and ['uom'], as well as manage the template Conversion chain
        self.set_degf(self.DEF_DEGF)

        return

    @staticmethod
    def code_name():
        return 'TemplateTemperature'

    @staticmethod
    def code_version():
        return __version__

    def set_degf(self, value):
        """
        Set F or C, which affects self['degc'] and ['uom']. Also, will make sure correct DegX conversion function
        is in the data_template, and the incorrect one is not in the data_template!

        :param value:
        :type value: bool
        :return:
        """
        self['degf'] = bool(value)
        if value:
            # then we want DegF
            self['uom'] = 'F'
            # remove any DegC/DegF conversion, add a DegF conversion
            self.remove_conversion(ConversionDegC.code_name())
            self.remove_conversion(ConversionDegF.code_name())
            self.add_conversion(ConversionDegF())

        else:  # we want DegC
            self['uom'] = 'C'
            # remove any DegF/DegC conversion, add a DegC conversion
            self.remove_conversion(ConversionDegF.code_name())
            self.remove_conversion(ConversionDegC.code_name())
            self.add_conversion(ConversionDegC())
        return
