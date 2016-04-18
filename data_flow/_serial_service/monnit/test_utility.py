# Test the Monnit Protocol code

import unittest
import logging
import time

import monnit.utility as utility
# from common.format_bytes import format_bytes


class TestUtility(unittest.TestCase):

    def test_monnit_utc(self):

        logging.debug("Test monnit UTC")

        # now = Fri Dec 18 16:20:00 2015
        now = time.mktime((2015, 12, 18, 16, 20, 0, 0, 0, 0)) + time.timezone
        # now_struct = time.strptime("2015-12-18 16:20:00 +0", "%Y-%m-%d %H:%M:%S %z")
        # now = time.mktime(now_struct)
        logging.debug("now {0}".format(time.ctime(now)))
        self.assertEqual(now, 1450506000.0)

        show = utility.format_timestamp(now)
        logging.debug("now {0}".format(show))
        self.assertEqual(show, "2015-12-18 23:20:00 UTC")
        show = utility.format_timestamp(now, true_iso=True)
        logging.debug("now {0}".format(show))
        self.assertEqual(show, "2015-12-18T23:20:00Z")

        # logging.debug("epoch {0}".format(utility.MONNIT_EPOCH))
        self.assertEqual(utility.MONNIT_EPOCH, 1262329200.0)

        now_monnit = utility.get_monnit_utc_float(now)
        # logging.debug("monnit {0}".format(now_monnit))
        # logging.debug("monnit 0x%08X" % int(now_monnit))
        self.assertEqual(now_monnit, 188151600.0)

        now_bytes = utility.get_monnit_utc_le32(now)
        # logging.debug("byte {0}".format(format_bytes("le32", now_bytes)))
        self.assertEqual(now_bytes, b"\xA0\x94\x74\x56")

        return


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
