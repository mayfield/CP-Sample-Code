# Test the DATA_Attributes

import unittest

from data.data_attribute import DataAttributeHandler, BooleanAttributeHandler


class TestAttributes(unittest.TestCase):

    def test_data_name(self):

        handler = DataAttributeHandler()
        attributes = dict()

        # 'data_name': {'data_type': IndexString},
        value1 = 'Hello'
        tag_name = 'data_name'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1.lower())
        # print("Attributes:{0}".format(attributes))

        value1 = 'hello_tome'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        value1 = 'hello-tome'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # spaces are not allowed
        value2 = 'This is the high-limit value'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1.lower())
        # print("Attributes:{0}".format(attributes))

        # other special char also not allowed
        value2 = 'Hello\r'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # this will error, as one cannot 'delete'
        value2 = ''
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # this will error, as one cannot 'delete'
        value2 = None
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # we cannot check uniqueness

        return

    def test_display_name(self):

        handler = DataAttributeHandler()
        attributes = dict()

        # 'display_name': {'data_type': UserString},
        value1 = 'Hello!'
        tag_name = 'display_name'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        value1 = 'This is the high-limit value'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        value2 = 'This is the high-limit value\r'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # this should clear out the value
        value2 = ''
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        # put something back in
        value1 = 'Hello!'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # this should clear out the value again
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        # toss a bogus attribute in - no error, but return in False
        value1 = 'Hello!'
        self.assertFalse(handler.set_attribute(attributes, 'silly_shoes!', value1))
        self.assertTrue(tag_name not in attributes)
        self.assertTrue('silly_shoes!' not in attributes)
        # print("Attributes:{0}".format(attributes))

        return

    def test_description(self):

        handler = DataAttributeHandler()
        attributes = dict()

        # 'description': {'data_type': UserString},
        value1 = 'Hello!'
        tag_name = 'description'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        value1 = 'This is the high-limit value'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        value2 = 'This is the high-limit value\r'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # this should clear out the value
        value2 = ''
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        # put something back in
        value1 = 'Hello!'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        # print("Attributes:{0}".format(attributes))

        # this should clear out the value again
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        # toss a bogus attribute in - no error, but return in False
        value1 = 'Hello!'
        self.assertFalse(handler.set_attribute(attributes, 'silly_shoes!', value1))
        self.assertTrue(tag_name not in attributes)
        self.assertTrue('silly_shoes!' not in attributes)
        # print("Attributes:{0}".format(attributes))

        return

    def test_display_color(self):

        handler = DataAttributeHandler()
        attributes = dict()

        # we support the CSS3 set of colors, so like 'beige', 'bisque', 'black', 'blue'

        tag_name = 'display_color'

        # 'display_color': {'data_type': str},
        value1 = 'coral'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # try a double-quoted value, single quotes
        value2 = "\'coral\'"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # try a double-quoted value, double quotes
        value2 = "\"coral\""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # mixed case
        value2 = "Coral"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        value2 = "CORAL"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # this should clear out value, put back to 'defaults'
        value2 = ""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        value1 = '(coral,navy)'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name].get_name(), ('coral', 'navy'))

        # this should clear out value, put back to 'defaults'
        value2 = ""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        # assume test_colors.py handles more of the diverse double entry values

        return

    def test_font_scale(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'font_scale'

        # 'font_scale': {'data_type': float},
        #  FONT_SCALE_LIST = (50, 75, 100, 125, 150)

        value1 = 100
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], float(value1))

        # bad type
        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], float(value1))

        # bad value
        value2 = 99
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], float(value1))

        value1 = 50.0
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], float(value1))

        value1 = 75.0
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], float(value1))

        value1 = 100.0
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], float(value1))

        value1 = 125.0
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], float(value1))

        value1 = 150.0
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], float(value1))

        # this should clear out value
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        value_expect = 125.0
        value1 = "125"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        value1 = "125.0"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        value1 = "  125.0 "
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        value1 = "\"125\""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        return

    def test_data_type(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'data_type'
        value_tag = 'value_type'

        # 'data_type': {'data_type': str},
        # DATA_TYPE_LIST = ('base', 'string', 'digital', 'gps', 'analog')

        value1 = 'base'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        self.assertEqual(attributes[value_tag], None)

        # bad type
        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        self.assertEqual(attributes[value_tag], None)

        # this should clear out value
        value2 = None
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        self.assertEqual(attributes[value_tag], None)

        value1 = 'string'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        self.assertEqual(attributes[value_tag], str)

        value1 = 'digital'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        self.assertEqual(attributes[value_tag], bool)

        value1 = 'analog'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        self.assertEqual(attributes[value_tag], float)

        # to be revisited when GPS type filled out
        value1 = 'gps'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)
        self.assertEqual(attributes[value_tag], str)
        # print("Attributes:{0}".format(attributes))

        return

    def test_value_type(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'value_type'

        # this is ALWAYS erro,we we control via ['data_ty[e'], not 'value_type'
        value1 = float
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value1)
        self.assertTrue(tag_name not in attributes)

        return

    def test_failsafe(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'failsafe'
        print("")

        # 'failsafe': {'data_type': None},

        # handle the base type, which has NO value, so no failsafe
        type_value = 'base'
        self.assertTrue(handler.set_attribute(attributes, 'data_type', type_value))
        self.assertEqual(attributes['data_type'], type_value)
        self.assertEqual(attributes['value_type'], None)

        value1 = True
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value1)
        self.assertTrue(tag_name not in attributes)

        value1 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertTrue(tag_name not in attributes)
        # self.assertEqual(attributes[tag_name], None)

        # handle the string type, which allows any value, converted to string
        type_value = 'string'
        self.assertTrue(handler.set_attribute(attributes, 'data_type', type_value))
        self.assertEqual(attributes['data_type'], type_value)
        self.assertEqual(attributes['value_type'], str)

        value1 = True
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], "True")

        value1 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertTrue(tag_name not in attributes)
        # self.assertEqual(attributes[tag_name], None)

        value1 = 99
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], "99")

        value1 = 12.34
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], "12.34")

        # handle the digital type, which allows any bool or int value
        type_value = 'digital'
        self.assertTrue(handler.set_attribute(attributes, 'data_type', type_value))
        self.assertEqual(attributes['data_type'], type_value)
        self.assertEqual(attributes['value_type'], bool)
        print("Attributes:{0}".format(attributes))

        value1 = True
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], True)
        print("Attributes:{0}".format(attributes))

        value1 = False
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], False)
        print("Attributes:{0}".format(attributes))

        value1 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertTrue(tag_name not in attributes)
        # self.assertEqual(attributes[tag_name], None)
        print("Attributes:{0}".format(attributes))

        value1 = "true"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], True)
        print("Attributes:{0}".format(attributes))

        value1 = " False"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], False)
        print("Attributes:{0}".format(attributes))

        value1 = 0
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], False)
        print("Attributes:{0}".format(attributes))

        value1 = 99
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], True)
        print("Attributes:{0}".format(attributes))

        value1 = 12.34
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value1)
        self.assertEqual(attributes[tag_name], True)  # is no change
        print("Attributes:{0}".format(attributes))

        value1 = "Sloppy sails"
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value1)
        self.assertEqual(attributes[tag_name], True)  # is no change
        print("Attributes:{0}".format(attributes))

        # type_value = 'gps'

        # handle the analog type, which allows any numeric value, converted to analog
        type_value = 'analog'
        self.assertTrue(handler.set_attribute(attributes, 'data_type', type_value))
        self.assertEqual(attributes['data_type'], type_value)
        self.assertEqual(attributes['value_type'], float)
        print("Attributes:{0}".format(attributes))

        value1 = 99
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], 99.0)
        print("Attributes:{0}".format(attributes))

        value1 = 0
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], 0.0)
        print("Attributes:{0}".format(attributes))

        value1 = 123.45
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], 123.45)
        print("Attributes:{0}".format(attributes))

        value2 = True
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        print("Attributes:{0}".format(attributes))

        value1 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertTrue(tag_name not in attributes)
        print("Attributes:{0}".format(attributes))

        value1 = 99
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], 99.0)
        print("Attributes:{0}".format(attributes))

        value2 = "true"
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)
        print("Attributes:{0}".format(attributes))

        value2 = "Sloppy sails"
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)  # is no change
        print("Attributes:{0}".format(attributes))

        return

    def test_attach_gps(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'attach_gps'

        # 'attach_gps': {'data_type': bool},

        value1 = True
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value1 = False
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        # bad type
        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out value
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        value_expect = True
        value1 = "TRUE"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        value1 = " TRUE  "
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        value1 = "\" TRUE\""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)
        # print("Attributes:{0}".format(attributes))

        return

    def test_read_only(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'read_only'

        # 'read_only': {'data_type': bool},

        value1 = True
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value1 = False
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        # bad type
        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out value
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        value_expect = True
        value1 = "TRUE"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        value1 = " TRUE  "
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)

        value1 = "\" TRUE\""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value_expect)
        # print("Attributes:{0}".format(attributes))

        return

    def test_display_name_true(self):

        handler = BooleanAttributeHandler()
        attributes = dict()

        tag_name = 'display_name_true'
        # 'display_name_true': {'data_type': IndexString},

        value1 = 'Hello!'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value1 = 'This is the high-limit value'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value2 = 'This is the high-limit value\r'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out the value
        value2 = ''
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        # put something back in
        value1 = 'Hello!'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out the value again
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        return

    def test_display_name_false(self):

        handler = BooleanAttributeHandler()
        attributes = dict()

        tag_name = 'display_name_false'
        # 'display_name_false': {'data_type': IndexString},

        value1 = 'Hello!'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value1 = 'This is the high-limit value'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value2 = 'This is the high-limit value\r'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out the value
        value2 = ''
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        # put something back in
        value1 = 'Hello!'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out the value again
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        return

    def test_display_color_true(self):

        handler = BooleanAttributeHandler()
        attributes = dict()

        # we support the CSS3 set of colors, so like 'beige', 'bisque', 'black', 'blue'

        tag_name = 'display_color_true'
        # 'display_color_true': {'data_type': DataColor},

        value1 = 'coral'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # mixed case
        value2 = "Coral"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # this should clear out value, put back to 'defaults'
        value2 = ""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        value1 = '(coral,navy)'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name].get_name(), ('coral', 'navy'))

        # this should clear out value, put back to 'defaults'
        value2 = ""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        # assume test_colors.py handles more of the diverse double entry values

        return

    def test_display_color_false(self):

        handler = BooleanAttributeHandler()
        attributes = dict()

        # we support the CSS3 set of colors, so like 'beige', 'bisque', 'black', 'blue'

        tag_name = 'display_color_false'
        # 'display_color_false': {'data_type': DataColor},

        value1 = 'coral'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # mixed case
        value2 = "Coral"
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertEqual(attributes[tag_name].get_name(), value1)

        # this should clear out value, put back to 'defaults'
        value2 = ""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        value1 = '(coral,navy)'
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name].get_name(), ('coral', 'navy'))

        # this should clear out value, put back to 'defaults'
        value2 = ""
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)
        # print("Attributes:{0}".format(attributes))

        # assume test_colors.py handles more of the diverse double entry values

        return

    def test_invert(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'invert'
        # 'invert': {'data_type': Digital},

        value1 = False
        self.assertFalse(handler.set_attribute(attributes, tag_name, value1))
        self.assertTrue(tag_name not in attributes)

        handler = BooleanAttributeHandler()

        value1 = True
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value1 = False
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        # bad type
        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out value
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        return

    def test_abnormal_when(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'abnormal_when'
        # 'abnormal_when': {'data_type': Digital},

        value1 = False
        self.assertFalse(handler.set_attribute(attributes, tag_name, value1))
        self.assertTrue(tag_name not in attributes)

        # 'auto_reset': {'data_type': Digital},
        # 'debounce_delay': {'data_type': Numeric},

        handler = BooleanAttributeHandler()

        value1 = True
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value1 = False
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        # bad type
        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out value
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        return

    def test_auto_reset(self):

        handler = DataAttributeHandler()
        attributes = dict()

        tag_name = 'auto_reset'
        # 'auto_reset': {'data_type': Digital}

        value1 = False
        self.assertFalse(handler.set_attribute(attributes, tag_name, value1))
        self.assertTrue(tag_name not in attributes)

        handler = BooleanAttributeHandler()

        value1 = True
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        value1 = False
        self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
        self.assertEqual(attributes[tag_name], value1)

        # bad type
        value2 = 'blue shoes'
        with self.assertRaises(ValueError):
            handler.set_attribute(attributes, tag_name, value2)
        self.assertEqual(attributes[tag_name], value1)

        # this should clear out value
        value2 = None
        self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
        self.assertTrue(tag_name not in attributes)

        return

        # TODO 'debounce_delay': {'data_type': Numeric}

    # def test_latitude(self):
    #
    #     handler = DataAttributeHandler()
    #     attributes = dict()
    #
    #     tag_name = 'latitude'
    #     # 'latitude': {'data_type': Numeric},
    #     # 'longitude': {'data_type': Numeric},
    #     # 'latitude_filter': {'data_type': Numeric},
    #     # 'longitude_filter': {'data_type': Numeric},
    #     # 'ground_speed_filter': {'data_type': Numeric},
    #     # 'is_move_cutoff': {'data_type': Numeric},
    #     # 'gps_mode': {'data_type': UserString},
    #
    #     value1 = False
    #     self.assertFalse(handler.set_attribute(attributes, tag_name, value1))
    #     self.assertTrue(tag_name not in attributes)
    #
    #     handler = BooleanAttributeHandler()
    #
    #     value1 = True
    #     self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
    #     self.assertEqual(attributes[tag_name], value1)
    #
    #     value1 = False
    #     self.assertTrue(handler.set_attribute(attributes, tag_name, value1))
    #     self.assertEqual(attributes[tag_name], value1)
    #
    #     # bad type
    #     value2 = 'blue shoes'
    #     with self.assertRaises(ValueError):
    #         handler.set_attribute(attributes, tag_name, value2)
    #     self.assertEqual(attributes[tag_name], value1)
    #
    #     # this should clear out value
    #     value2 = None
    #     self.assertTrue(handler.set_attribute(attributes, tag_name, value2))
    #     self.assertTrue(tag_name not in attributes)
    #
    #     return


if __name__ == '__main__':
    unittest.main()
