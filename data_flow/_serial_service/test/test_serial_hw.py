__author__ = 'Lynn'

import unittest

import serial_hw

ASSUME_PORT = "COM5"

class TestSerialHw(unittest.TestCase):

    def test_basic(self):
        obj = serial_hw.SerialHardware(0)
        
        
        return

    #    self.assertFalse(obj.product_has_ri_in(obj._product))
    #    self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
    #     with self.assertRaises(ValueError):
    #         # we assume 'bad_param' has not become a valid value!
    #         obj.set_decoding('bad_param')
    #
    #     self.assertTrue('FOO'.isupper())

if __name__ == '__main__':
    unittest.main()
