# Test the Monnit Protocol code

import unittest
import logging

import monnit.protocol as protocol


class TestProtocol(unittest.TestCase):

    def test_update_network_state_req(self):

        obj = protocol.MonnitProtocol()

        messages_list = [
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
            b'\xc5\x06\x00\x22\xb4\x74\x01\x00\x57',
            b'\xC5\x0C\x00\x23\xC8\x00\x00\x00\x02\x00\x07\x80\x01\x30\x6C',
            b'\xC5\x07\x00\x24\x85\x03\x00\x00\x00\x7F',
            b'\xC5\x07\x00\x24\xC8\x00\x00\x00\x0C\x3D',
            b'\xc5\x0c\x00\x23\xc8\x00\x00\x00\x03\x00\x15\x44\x01\x30\xc3',
            b'\xc5\x0e\x00\x52\xc8\x00\x00\x00\xc8\x00\x00\x00\x02\x05\x00\x00\xa5',
            b'\xc5\x12\x02\x56\x02\x77\x01\x00\x00\x00\x00\x00\xd7\xd7\xa4\x02\x00\x22\xf2\xd8\xe7',
            b'\xc5\x12\x00\x56\xb4\x74\x01\x00\x00\x00\x00\x00\xd1\xd1\xa1\x09\x00\x00\x01\x00\x58',
            b'\xc5\x12\x02\x56\xb4\x74\x01\x00\x00\x00\x00\x00\xd1\xd1\xa1\x09\x00\x02\x00\x00\x7b',
            b'\xc5\x12\x00\x56\xb4\x74\x01\x00\x00\x00\x00\x00\xd2\xd2\xa1\x09\x00\x00\x01\x00\x1c',
            b'\xc5\x12\x02\x56\xb4\x74\x01\x00\x00\x00\x00\x00\xcb\xcb\xa0\x09\x00\x02\x00\x00\xd0',
            b'\xc5\x11\x00\x56\xb5\x74\x01\x00\x00\x00\x00\x00\xc2\xc2\xa4\x03\x00\x00\x00\x49',
        ]

        logging.debug("Test good")
        for message in messages_list:
            obj.parse_message(message)
            # logging.debug("Test {0}".format(message))
            # result = obj.parse_message(message)
            # logging.debug("Result {0}".format(result))

        return

    def test_formats(self):

        obj = protocol.MonnitProtocol()
        obj.set_gateway_address(200)
        obj.add_sensor_id(95412)
        obj.add_sensor_id(95413)
        obj.add_sensor_id(96002)

        result = obj._format_x21_update_network_state(b'\x00', b'\x22\x63\x3b\x0b')
        expect = b'\xC5\x07\x00\x21\x00\x22\x63\x3b\x0B\xB1'
        self.assertEqual(result, expect)

        result = obj._format_x21_update_network_state(b'\x01', b'\x39\xB5\x31\x0b')
        expect = b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E'
        # logging.debug("See    {0}".format(result))
        # logging.debug("Expect {0}".format(expect))
        self.assertEqual(result, expect)

        result = obj._format_x22_register_device(95412)
        expect = b'\xc5\x06\x00\x22\xb4\x74\x01\x00\x57'
        self.assertEqual(result, expect)

        result = obj._format_x22_register_device(95413)
        expect = b'\xc5\x06\x00\x22\xb5\x74\x01\x00\x2e'
        self.assertEqual(result, expect)

        result = obj._format_x22_register_device(96002)
        expect = b'\xc5\x06\x00\x22\x02\x77\x01\x00\xf3'
        self.assertEqual(result, expect)

        result = obj._format_x22_register_device(96002)
        expect = b'\xc5\x06\x00\x22\x02\x77\x01\x00\xf3'
        self.assertEqual(result, expect)

        # this forces index/counter to 0
        result = obj._format_x24_queued_message_req(0)
        expect = b'\xc5\x07\x00\x24\xc8\x00\x00\x00\x00\x85'
        self.assertEqual(result, expect)

        # will be 0 + 1 = 1
        result = obj._format_x24_queued_message_req()
        expect = b'\xc5\x07\x00\x24\xc8\x00\x00\x00\x01\x12'
        self.assertEqual(result, expect)

        # will be 1 + 1 = 2
        result = obj._format_x24_queued_message_req()
        expect = b'\xc5\x07\x00\x24\xc8\x00\x00\x00\x02\x3c'
        self.assertEqual(result, expect)

        # this forces index/counter to 255 (the max)
        result = obj._format_x24_queued_message_req(255)
        expect = b'\xc5\x07\x00\x24\xc8\x00\x00\x00\xFF\xB9'
        self.assertEqual(result, expect)

        # will wrap to 0
        result = obj._format_x24_queued_message_req()
        expect = b'\xc5\x07\x00\x24\xc8\x00\x00\x00\x00\x85'
        # logging.debug("See    {0}".format(result))
        # logging.debug("Expect {0}".format(expect))
        self.assertEqual(result, expect)

        return


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
