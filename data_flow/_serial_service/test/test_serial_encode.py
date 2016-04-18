__author__ = 'Lynn'

import unittest

import serial_encode


class TestSerialEncode(unittest.TestCase):

    TEST_STRING = "If you believe that truth=beauty,\r\nthen surely peach tree is the most beautiful rock-head\r\n"

    TEST_BYTES = b"If you believe that truth=beauty,\r\nthen surely peach tree is the most beautiful rock-head\r\n"

    def test_binary(self):
        net_string = serial_encode.to_net_binary(self.TEST_STRING)
        restored_string = serial_encode.from_net_binary(net_string)
        self.assertEqual(restored_string, self.TEST_STRING)

    def test_unicode(self):
        net_string = serial_encode.to_net_unicode(self.TEST_STRING)
        restored_string = serial_encode.from_net_unicode(net_string)
        self.assertEqual(restored_string, self.TEST_STRING)

    def test_quoted(self):
        net_string = serial_encode.to_net_quoted(self.TEST_STRING)
        restored_string = serial_encode.from_net_quoted(net_string)
        self.assertEqual(restored_string, self.TEST_STRING)

    def test_hexascii(self):
        net_string = serial_encode.to_net_hexascii(self.TEST_STRING)
        restored_string = serial_encode.from_net_hexascii(net_string)
        self.assertEqual(restored_string, self.TEST_STRING)

    def test_base64(self):
        net_string = serial_encode.to_net_base64(self.TEST_STRING)
        restored_string = serial_encode.from_net_base64(net_string)
        self.assertEqual(restored_string, self.TEST_STRING)

    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()
