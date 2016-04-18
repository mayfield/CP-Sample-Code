import logging
import logging.handlers
import sys
import time

import unittest
from common.wipipe import WiPipeHandler


USER_INFO = "admin:441b1702"
GWAY_IP = "192.168.1.1"


class TestApiHandler(unittest.TestCase):

    def test_validate_path(self):

        obj = WiPipeHandler()

        with self.assertRaises(TypeError):
            obj._normalize_path(None)

        with self.assertRaises(TypeError):
            obj._normalize_path(10)

        # confirm the '/api' is tacked on
        expect = '/api/status/gpio'
        self.assertEqual(obj._normalize_path('status/gpio'), expect)
        self.assertEqual(obj._normalize_path('/status/gpio'), expect)
        self.assertEqual(obj._normalize_path('api/status/gpio'), expect)
        self.assertEqual(obj._normalize_path('/api/status/gpio'), expect)

        # confirm the '/api' is tacked removed
        expect = 'status/gpio'
        self.assertEqual(obj._normalize_path('status/gpio', add_base=False), expect)
        self.assertEqual(obj._normalize_path('/status/gpio', add_base=False), expect)
        self.assertEqual(obj._normalize_path('api/status/gpio', add_base=False), expect)
        self.assertEqual(obj._normalize_path('/api/status/gpio', add_base=False), expect)

        return

    def test_get_topic(self):

        obj = WiPipeHandler()
        obj.trace = logger

        obj.set_user_name("admin")
        obj.set_password("441b1702")
        obj.set_ip_address("192.168.1.1")

        expect = "http://192.168.1.1"
        # expect = "admin:441b1702@192.168.1.1"
        self.assertEqual(obj.url, expect)

        self.assertEqual(obj._user_name, "admin")
        self.assertEqual(obj._password, "441b1702")

        # data = obj.get_topic('status/gpio')
        # print(data)
        #
        # data = obj.get_topic('status/hello')
        # print(data)

        # data = obj.get_topic('status/gpio/LED_POWER')
        # print(data)

        return

    def test_put_topic(self):

        obj = WiPipeHandler()
        obj.trace = logger

        obj.set_user_name("admin")
        obj.set_password("441b1702")
        obj.set_ip_address("192.168.1.1")

        data = obj.get_topic('control/gpio')
        print(data)

        if False:
            data = obj.put_topic('status/gpio/LED_POWER', 1)
            print(data)

        return


def make_logger():
    global logger

    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    destination = ('192.168.0.10', 514)
    try:
        if sys.argv[1]:
            destination = ('localhost', 514)

    except:
        destination = ('192.168.0.10', 514)

    handler = logging.handlers.SysLogHandler(address=destination)
    logger.info("Handler SysLog(%s)" % str(destination))

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    logger.info("Start %s" % time.strftime("%H:%M:%S", time.localtime()))

    return

if __name__ == '__main__':
    global logger

    logger = logging.getLogger('test')
    make_logger()

    unittest.main()
