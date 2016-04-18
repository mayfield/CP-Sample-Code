# Test the PARSE DATA module

import unittest

from data.data_sample import DataSample


class TestDataSample(unittest.TestCase):

    def test_data_type_python_to_internal(self):

        obj = DataSample()

        value = 0
        obj.set_value(value)
        self.assertEqual(obj.get_value(), value)

        value = 7.4
        obj.set_value(value)
        self.assertEqual(obj.get_value(), value)

        value = 'stop'
        obj.set_value(value)
        self.assertEqual(obj.get_value(), value)

        return

if __name__ == '__main__':
    unittest.main()
