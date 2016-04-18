# Test the DATA_COLOR, which supports CSS3 names

import unittest

from data.data_color import DataColor


class TestAttributes(unittest.TestCase):

    def test_set(self):

        obj = DataColor()

        # we support the CSS3 set of colors, so like 'beige', 'bisque', 'black', 'blue', 'royalblue'

        value_lower = 'coral'
        obj.set(value_lower)
        self.assertEqual(obj.get_name(), value_lower)

        # bad value
        value = 'blue shoes'
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_lower)

        # try a double-quoted value, single quotes
        value = "\'coral\'"
        obj.set(value)
        self.assertEqual(obj.get_name(), value_lower)

        # try a double-quoted value, double quotes
        value = "\"coral\""
        obj.set(value)
        self.assertEqual(obj.get_name(), value_lower)

        # mixed case
        value = "Coral"
        obj.set(value)
        self.assertEqual(obj.get_name(), value_lower)

        value = "CORAL"
        obj.set(value)
        self.assertEqual(obj.get_name(), value_lower)

        # this should clear out value, put back to 'defaults'
        value = ""
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_lower)

        value_tuple = ('coral', 'navy')

        value = '(coral,navy)'
        obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = '(coral, navy) '
        obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = '(Coral, NAVY)'
        obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = '("Coral",navy)'
        obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = '(coral,"navy")'
        obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = "('coral',navy)"
        obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        # test bad name
        value = "('royal blue',coral)"
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = "(doggy,coral)"
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = "(coral,silly)"
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        # test empty entry
        value = "(,'coral')"
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        value = "('coral',)"
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        # more than 2 is bad
        value = "(coral,navy,red)"
        with self.assertRaises(ValueError):
            obj.set(value)
        self.assertEqual(obj.get_name(), value_tuple)

        return


if __name__ == '__main__':
    unittest.main()
