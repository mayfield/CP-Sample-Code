# Test the DATA_PRECISION

import unittest

from cp_lib.data.data_precision import validate_precision_value, \
    get_precision_string_format, \
    use_precision_to_reduce_value, use_precision_to_string


class TestDataPrecision(unittest.TestCase):

    def test_string_format(self):

        value = 7256.63729

        precision = 0.0001
        self.assertTrue(validate_precision_value(precision))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%0.4f")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7256.6373)
        self.assertEqual(format_source % value, "7256.6373")

        precision = 0.001
        self.assertTrue(validate_precision_value(precision))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%0.3f")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7256.637)
        self.assertEqual(format_source % value, "7256.637")

        precision = 0.01
        self.assertTrue(validate_precision_value(precision))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%0.2f")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7256.64)
        self.assertEqual(format_source % value, "7256.64")

        precision = 0.1
        self.assertTrue(validate_precision_value(precision))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%0.1f")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7256.6)
        self.assertEqual(format_source % value, "7256.6")

        precision = 1.0
        self.assertTrue(validate_precision_value(precision))
        self.assertTrue(validate_precision_value(int(precision)))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%d")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7257.0)
        self.assertEqual(use_precision_to_string(precision, value), "7257")

        precision = 10.0
        self.assertTrue(validate_precision_value(precision))
        self.assertTrue(validate_precision_value(int(precision)))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%d")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7260.0)
        self.assertEqual(use_precision_to_string(precision, value), "7260")

        precision = 100.0
        self.assertTrue(validate_precision_value(precision))
        self.assertTrue(validate_precision_value(int(precision)))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%d")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7300.0)
        self.assertEqual(use_precision_to_string(precision, value), "7300")

        precision = 1000.0
        self.assertTrue(validate_precision_value(precision))
        self.assertTrue(validate_precision_value(int(precision)))
        format_source = get_precision_string_format(precision)
        self.assertEqual(format_source, "%d")
        self.assertEqual(use_precision_to_reduce_value(precision, value),
                         7000.0)
        self.assertEqual(use_precision_to_string(precision, value), "7000")

        self.assertFalse(validate_precision_value(0.00001))
        self.assertFalse(validate_precision_value(0.05))
        self.assertFalse(validate_precision_value(23.5))
        self.assertFalse(validate_precision_value(10000))

        with self.assertRaises(ValueError):
            get_precision_string_format(0.00001)
            get_precision_string_format(0.05)
            get_precision_string_format(23.5)
            get_precision_string_format(10000)

        return

if __name__ == '__main__':
    unittest.main()
