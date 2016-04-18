__author__ = 'Lynn'

import unittest
import time

import serial_object
import serial_encode
import serial_settings


class TestSerialObject(unittest.TestCase):

    def test_simple_echo(self):
        obj = serial_object.SerialObject(0)
        
        now = time.time()
        with self.assertRaises(serial_object.SerialObjectException):
            # echo port is NOT open!
            obj.write('bad_param', now)

        self.assertEqual(obj.state, obj.STATE_DEFAULT)
        self.assertTrue(obj.open())
        self.assertEqual(obj.state, obj.STATE_ACTIVE)
        
        message1 = b'Hello'
        result = obj.write(message1, now)
        self.assertEqual(result, len(message1))

        message2 = b' World!'
        message_n = message1 + message2
        now += 1
        result = obj.write(message2, now)
        self.assertEqual(result, len(message2))
        peek = obj.recv_buffer.data_peek()
        self.assertEqual(len(peek), len(message_n))
        self.assertEqual(obj.get_buffer_size(), len(message_n))

        result = obj.read(now)
        self.assertEqual(result, message_n)
        self.assertEqual(obj.get_buffer_size(), 0)

        return
        
if __name__ == '__main__':
    unittest.main()
