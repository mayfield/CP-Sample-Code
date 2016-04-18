# File: data_color.py
# Desc: abstract the colors used to display data - use common HTML/CSS RGB tuples

import common.parse_data as parse_data
import common.webcolors as colors

__version__ = "1.1.0"

# History:
#
# 1.0.0: 2015-Aug Lynn
#       * initial draft
#


class DataColor(object):
    """
    Abstract the data colors for data, which are the 140 values by CSS3
    """

    DEF_SINGLE = True
    DEF_NAME = 'white'
    DEF_HEX = '#FFFFFF'

    def __init__(self, value=None):
        self.single = self.DEF_SINGLE
        self.name = self.DEF_NAME
        self.hex = self.DEF_HEX

        if value is not None:
            self.set(value)
        return

    @staticmethod
    def code_name():
        return 'DataColor'

    @staticmethod
    def code_version():
        return __version__

    def __repr__(self):
        """
        this is either:
        - if single, a name like "coral"
        - if double, is a string of tuple, such as "(white,black)"
        :return:
        """
        return str(self.name)

    def get_name(self):
        return self.name

    def get_hex(self):
        return self.hex

    def set(self, color):
        """
        Given a color as "aqua" or ("aqua", "white") or "(aqua,white)", set as single or double

        :param color: the name of HEX string to input
        :type color: str or tuple
        """
        if color is not None and color != "":  # None is an error - we cannot 'clear'
            if isinstance(color, str):
                color = color.strip()
                if color[0] == '(':
                    # then assume is (back,fore)
                    color = color[1:-1]
                    color = color.split(',')
                    if len(color) == 2:
                        self.set_double(color[0], color[1])
                        return

                else:  # assume is like "aqua"
                    self.set_single(color)
                    return

            if type(color) in (tuple, list) and len(color) == 2:
                self.set_double(color[0], color[1])
                return

        raise ValueError("bad color input:\"{0}\"".format(color))

    def set_single(self, back_color):
        """
        Set the color with a CSS3 name or hex string
        """
        self.single = True
        back_name, back_hex = self._lookup(back_color)

        # if still here, name was okay
        self.name = back_name
        self.hex = back_hex
        return

    def set_double(self, back_color, fore_color):
        """
        Set the color with a CSS3 name or hex string
        """
        self.single = False

        back_name, back_hex = self._lookup(back_color)
        fore_name, fore_hex = self._lookup(fore_color)

        # if still here, name was okay
        self.name = (back_name, fore_name)
        self.hex = (back_hex, fore_hex)
        return

    def _lookup(self, one_color):
        """
        convert a color (name or hex) to a known tuple
        """
        if one_color is None or one_color == "":
            raise ValueError("bad color input:\"{0}\"".format(one_color))

        if isinstance(one_color, int):
            one_color = '#' + "%06X" % one_color

        # trim white space, and any leading/trailing quotes
        one_color = parse_data.clean_string(one_color)

        if one_color[0] == '#':
            # assume is hex string
            return self._lookup_by_hex(one_color)
        else:  # else assume is name string
            return self._lookup_by_name(one_color)

    @staticmethod
    def _lookup_by_name(name_value: str):
        """
        Set the color with a CSS3 name like aqua, bisque, etc.
        """
        # this throws ValueError if the name is not known
        name_value = name_value.lower()
        hex_value = colors.name_to_hex(name_value)
        # if still here, name was okay
        return name_value, hex_value

    @staticmethod
    def _lookup_by_hex(hex_value: str):
        """
        Set the color with a CSS3 hex string, like '#f0f8ff'
        """
        hex_value = hex_value.lower()
        # this throws ValueError if the HEX string is not known
        name_value = colors.hex_to_name(hex_value)
        # if still here, name was okay
        return name_value, hex_value
