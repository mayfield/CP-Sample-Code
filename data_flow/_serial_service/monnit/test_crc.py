# Test the Monnit CRC code

import unittest
import logging

import monnit.crc as crc


class TestCrc(unittest.TestCase):

    def test_crc(self):

        messages_list = [
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
            b'\xC5\x0C\x00\x23\xC8\x00\x00\x00\x02\x00\x07\x80\x01\x30\x6C',
            b'\xC5\x07\x00\x24\x85\x03\x00\x00\x00\x7F',
            b'\xC5\x07\x00\x24\xC8\x00\x00\x00\x0C\x3D'
        ]

        logging.debug("Test good CRC")
        for message in messages_list:
            # logging.debug("Test {0}".format(message))
            self.assertEqual(crc.crc_calculate(message), message[-1])

        logging.debug("Test NULL message")
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            crc.crc_calculate(None)

        logging.debug("Test short message")
        # messages must be at least <delm><len><opt><cmd><crc>
        messages_list = [
            b'',
            b'\xC5',
            b'\xC5\x0C',
            b'\xC5\x07\x00',
            b'\xC5\x07\x00\x24',
        ]
        for message in messages_list:
            # logging.debug("Test {0}".format(message))
            with self.assertRaises(ValueError):
                crc.crc_calculate(message)

        logging.debug("Test bad delimiter")
        messages_list = [
            b'\x00\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
            b'\xC4\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
            b'\xFF\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
        ]
        for message in messages_list:
            # logging.debug("Test {0}".format(message))
            with self.assertRaises(ValueError):
                crc.crc_calculate(message)

        logging.debug("Test good length")
        # CRC (\x1E) can be attached, or not (is optional)
        messages_list = [
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B',
        ]
        for message in messages_list:
            self.assertEqual(crc.crc_calculate(message), 0x1E)

        logging.debug("Test bad length")
        # one is too long by 1 byte; other is too short by 1 byte
        messages_list = [
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E\x00',
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31',
        ]
        for message in messages_list:
            with self.assertRaises(ValueError):
                crc.crc_calculate(message)

        logging.debug("Test crc_append CRC")
        messages_list = [
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B',
        ]
        for message in messages_list:
            result = crc.crc_append(message)
            self.assertEqual(messages_list[0], result)

        logging.debug("Test CRC crc_isvalid")
        # this message has good CRC
        messages_list = [
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E',
        ]
        for message in messages_list:
            # logging.debug("Test {0}".format(message))
            self.assertTrue(crc.crc_isvalid(message))

        # these messages have bad CRC
        messages_list = [
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\x1E\x00',
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31\x0B\xFF',
            b'\xC5\x07\x00\x21\x01\x39\xFF\x31\x0B\x1E',
            b'\xC5\x07\x00\x21\x01\x39\xB5\x31',
        ]
        for message in messages_list:
            with self.assertRaises(ValueError):
                crc.crc_isvalid(message)

        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
