# Test the iMonnit.com upload

import unittest
import logging
import time

from monnit.imonnit import ImonnitUpload


class TestImonnit(unittest.TestCase):

    def test_build_header(self):

        # noinspection PyUnresolvedReferences
        from common.format_bytes import format_bytes

        logging.info("Test build header")
        obj = ImonnitUpload()
        obj.set_apn_id(200)
        obj.increment_seq_no(use=5)

        result = obj._build_header()
        expect = b'\xC8\x00\x00\x00\x00\x00\x00\x00\x02\x05\x00\x00\x00\x00'
        self.assertEqual(result, expect)

        result = obj.build_upload()
        # same as above, but added uin16 for 0 count (& seq no increment 5 -> 6)
        expect = b'\xC8\x00\x00\x00\x00\x00\x00\x00\x02\x06\x00\x00\x00\x00\x00\x00'
        # logging.debug(format_bytes("result", result))
        # logging.debug(format_bytes("expect", expect))
        self.assertEqual(result, expect)

        return

    def test_add_queue(self):

        # noinspection PyUnresolvedReferences
        from common.format_bytes import format_bytes

        messages = [
            b'\xC5\x12\x02\x56\xB4\x74\x01\x00\x25\xF0\x53\x0B\xD7\xD7\x95\x09\x00\x02\x00\x00\xE0',
            b'\xC5\x11\x00\x56\xB5\x74\x01\x00\xE8\xF1\x53\x0B\xD3\xD3\xA2\x03\x00\x00\x00\x98',
            b'\xC5\x11\x00\x56\x01\x77\x01\x00\x6E\xFA\x53\x0B\xD5\xD5\x9D\x17\x00\x00\x00\x2C',
            b'\xC5\x11\x02\x56\x01\x77\x01\x00\x9D\xFA\x53\x0B\xD5\xD5\x9D\x17\x00\x02\x01\xB8',
        ]

        logging.info("Test adding to queue")
        obj = ImonnitUpload()
        obj.set_apn_id(200)
        obj.increment_seq_no(use=5)

        # start with nothing, so oldest time == 0
        self.assertEqual(obj.queue_size(), 0)
        self.assertEqual(obj.oldest_time, 0)
        self.assertEqual(obj.queue_age(), 0)

        obj.queue_message(messages[0])
        now = time.time()
        self.assertEqual(obj.queue_size(), 1)
        self.assertNotEqual(obj.oldest_time, 0)
        self.assertAlmostEqual(obj.oldest_time, now, places=1)
        save_oldest_time = obj.oldest_time

        # force a new time.time()
        time.sleep(1.1)

        obj.queue_message(messages[1])
        self.assertEqual(obj.queue_size(), 2)
        self.assertNotEqual(obj.oldest_time, 0)
        # confirm oldest_time is NOT change!
        self.assertEqual(obj.oldest_time, save_oldest_time)
        self.assertGreater(obj.queue_age(), 1.1)

        obj.queue_message(messages[2])
        self.assertEqual(obj.queue_size(), 3)
        self.assertNotEqual(obj.oldest_time, 0)
        self.assertEqual(obj.oldest_time, save_oldest_time)

        obj.queue_message(messages[3])
        self.assertEqual(obj.queue_size(), 4)
        self.assertNotEqual(obj.oldest_time, 0)
        self.assertEqual(obj.oldest_time, save_oldest_time)

        # now, try to build a full 4-message block with forced time & seq no = 5
        result = obj.build_upload(force_time=b'\x2B\x39\x58\x0B')
        expect = b'\xC8\x00\x00\x00\x00\x00\x00\x00\x02\x05\x00\x00\x00\x00' + \
                 b'\x04\x00\x2B\x39\x58\x0B'
        for data in messages:
            expect += data
        # logging.debug(format_bytes("result", result))
        logging.debug(format_bytes("expect", expect))
        self.assertEqual(result, expect)
        self.assertEqual(obj.queue_size(), 0)
        self.assertEqual(obj.oldest_time, 0)

        return

    def test_upload(self):

        # noinspection PyUnresolvedReferences
        from common.format_bytes import format_bytes

        messages = [
            b'\xC5\x12\x02\x56\xB4\x74\x01\x00\x25\xF0\x53\x0B\xD7\xD7\x95\x09\x00\x02\x00\x00\xE0',
            b'\xC5\x11\x00\x56\xB5\x74\x01\x00\xE8\xF1\x53\x0B\xD3\xD3\xA2\x03\x00\x00\x00\x98',
            b'\xC5\x11\x00\x56\x01\x77\x01\x00\x6E\xFA\x53\x0B\xD5\xD5\x9D\x17\x00\x00\x00\x2C',
            b'\xC5\x11\x02\x56\x01\x77\x01\x00\x9D\xFA\x53\x0B\xD5\xD5\x9D\x17\x00\x02\x01\xB8',
        ]

        logging.info("Test adding to queue")
        obj = ImonnitUpload()
        obj.set_apn_id(200)

        for message in messages:
            obj.queue_message(message)

        self.assertEqual(obj.queue_size(), 4)

        if True:
            # a simple enable/disable to eliminate 'internet access' dependency
            result = obj.do_upload(save=True)

            logging.debug(format_bytes("request", obj.saved_request))
            logging.debug(format_bytes("result", result))
            self.assertEqual(obj.queue_size(), 0)
            self.assertEqual(obj.oldest_time, 0)

        return


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
