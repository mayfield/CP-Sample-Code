__author__ = 'Lynn'

import unittest
import time

import serial_buffer
import serial_encode
import serial_settings


class TestSerialBuffer(unittest.TestCase):

    def test_decode_none(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(None)
        self.assertEqual(obj._in_coder, None)
        self.assertEqual(obj._out_coder, None)

    def test_decode_bad(self):
        obj = serial_buffer.SerialBuffer()
        with self.assertRaises(ValueError):
            # we assume 'bad_param' has not become a valid value!
            obj.set_decoding('bad_param')

    def test_decode_binary(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(serial_settings.NET_ENCODE_BINARY)
        # this is a special - case, we avoid the indirect method call (good? bad?)
        self.assertEqual(obj._in_coder, None)
        self.assertEqual(obj._out_coder, None)

    def test_decode_unicode(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(serial_settings.NET_ENCODE_UNICODE)
        self.assertEqual(obj._in_coder, serial_encode.from_net_unicode)
        self.assertEqual(obj._out_coder, serial_encode.to_net_unicode)

    def test_decode_quoted(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(serial_settings.NET_ENCODE_QUOTED)
        self.assertEqual(obj._in_coder, serial_encode.from_net_quoted)
        self.assertEqual(obj._out_coder, serial_encode.to_net_quoted)

    def test_decode_hexascii(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(serial_settings.NET_ENCODE_HEXASCII)
        self.assertEqual(obj._in_coder, serial_encode.from_net_hexascii)
        self.assertEqual(obj._out_coder, serial_encode.to_net_hexascii)
        
    def test_decode_base64(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(serial_settings.NET_ENCODE_BASE64)
        self.assertEqual(obj._in_coder, serial_encode.from_net_base64)
        self.assertEqual(obj._out_coder, serial_encode.to_net_base64)
        
    def test_decode_zip(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(serial_settings.NET_ENCODE_ZIP)
        self.assertEqual(obj._in_coder, serial_encode.from_net_zip)
        self.assertEqual(obj._out_coder, serial_encode.to_net_zip)
        
    def test_decode_gzip(self):
        obj = serial_buffer.SerialBuffer()
        obj.set_decoding(serial_settings.NET_ENCODE_GZIP)
        self.assertEqual(obj._in_coder, serial_encode.from_net_gzip)
        self.assertEqual(obj._out_coder, serial_encode.to_net_gzip)

    def test_eom_clear(self):
        obj = serial_buffer.SerialBuffer()
        self.assertEqual(obj.end_of_message, 
                         serial_buffer.SerialBuffer.default_end_of_message)
        obj.set_end_of_message_callback(None)
        self.assertEqual(obj.end_of_message, 
                         serial_buffer.SerialBuffer.default_end_of_message)
        return

    def test_simple_buffer(self):
        obj = serial_buffer.SerialBuffer()
        
        # we start with nothing, so things are default
        now = time.time()
        self.assertEqual(obj.recv_idle_pack_seconds, obj.DEF_IDLE_PACK)
        self.assertEqual(obj.last_data_time, 0)
        self.assertEqual(obj._recv_buffer, None)
        self.assertEqual(obj.total_wire_bytes_proc, 0)
        self.assertEqual(obj.total_raw_bytes_proc, 0)
        self.assertEqual(obj.total_segments_proc, 0)
        self.assertEqual(obj.total_messages_proc, 0)
        
        # we add the singe buffer, which is 5 bytes long
        message1 = b'Hello'
        result = obj.process(message1, now)
        self.assertEqual(result, None)
        self.assertEqual(obj.last_data_time, now)
        self.assertEqual(obj._recv_buffer, message1)
        self.assertEqual(obj.total_wire_bytes_proc, len(message1))
        self.assertEqual(obj.total_raw_bytes_proc, len(message1))
        self.assertEqual(obj.total_segments_proc, 1)
        self.assertEqual(obj.total_messages_proc, 0)

        # we increment time, but tick returns None since idle pack timeout isn't expired
        # the last_data_time should not change, is same as the older
        result = obj.tick(now)
        self.assertEqual(result, None)
        self.assertEqual(obj.last_data_time, now)
        self.assertEqual(obj._recv_buffer, message1)

        # we increment time, and tack 7 more bytes one, idle pack tout still not expired
        message2 = b' World!'
        messageN = message1 + message2
        now += 1
        result = obj.process(message2, now)
        self.assertEqual(result, None)
        self.assertEqual(obj.last_data_time, now)
        self.assertEqual(obj._recv_buffer, messageN)
        self.assertEqual(obj.total_wire_bytes_proc, len(messageN))
        self.assertEqual(obj.total_raw_bytes_proc, len(messageN))
        self.assertEqual(obj.total_segments_proc, 2)
        self.assertEqual(obj.total_messages_proc, 0)

        # we increment time by more than idle pack tout, so we know is expired
        # tick should return the accumulated buffer. We also incr a message total
        now += obj.DEF_IDLE_PACK + 1
        result = obj.tick(now)
        self.assertEqual(result, [messageN])
        self.assertEqual(obj._recv_buffer, None)
        self.assertEqual(obj.total_wire_bytes_proc, len(messageN))
        self.assertEqual(obj.total_raw_bytes_proc, len(messageN))
        self.assertEqual(obj.total_segments_proc, 2)
        self.assertEqual(obj.total_messages_proc, 1)

        return
        
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()
