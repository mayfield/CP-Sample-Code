__author__ = 'Lynn'

import unittest

from data.cp_api import ApiRouter
import serial_publish


class TestSerialPublish(unittest.TestCase):

    def test_validate_product_name(self):
        api = ApiRouter()
        obj = serial_publish.SerialStatsPublish('/status/serial_1/stats', api)

        obj._product = '8x0'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
        obj._product = '8X0'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
        obj._product = '800'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
        obj._product = '850'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
        obj._product = 'cba800'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
        obj._product = 'Cba800'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
        obj._product = 'CBA800'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
        obj._product = 'CBA850'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)

        obj._product = '11x0'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)
        obj._product = '11X0'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)
        obj._product = '1100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)
        obj._product = '1150'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)
        obj._product = 'ibr1100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)
        obj._product = 'Ibr1100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)
        obj._product = 'IBR1100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)
        obj._product = 'IBR1150'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_11X0)

        obj._product = '31x0'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)
        obj._product = '31X0'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)
        obj._product = '3100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)
        obj._product = '3150'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)
        obj._product = 'aer3100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)
        obj._product = 'Aer3100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)
        obj._product = 'AER3100'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)
        obj._product = 'AER3150'
        self.assertTrue(obj._validate_product_name_in_self())
        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_31X0)

        return

    def test_control_signals_8X0(self):
        api = ApiRouter()
        obj = serial_publish.SerialStatsPublish('/status/serial_1/stats', api)
        obj.set_product_support_details('8x0')

        # 800 only has RTS/CTS
        self.assertFalse(obj.product_has_dtrdsr(obj._product))
        self.assertTrue(obj.product_has_rtscts(obj._product))
        self.assertFalse(obj.product_has_cd_out(obj._product))
        self.assertFalse(obj.product_has_cd_in(obj._product))
        self.assertFalse(obj.product_has_ri_out(obj._product))
        self.assertFalse(obj.product_has_ri_in(obj._product))

        self.assertEqual(obj._product, serial_publish.SerialStatsPublish.PRODUCT_8X0)
    # def test_decode_bad(self):
    #     obj = serial_buffer.SerialBuffer()
    #     with self.assertRaises(ValueError):
    #         # we assume 'bad_param' has not become a valid value!
    #         obj.set_decoding('bad_param')
    #
        return
        
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()
