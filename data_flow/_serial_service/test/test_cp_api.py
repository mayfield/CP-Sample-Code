__author__ = 'Lynn'

import unittest

from data import cp_api


class TestCpApi(unittest.TestCase):

    def test_make_path(self):
        api = cp_api.ApiRouterDisk()
        path = "/data/serial/0/mode"
        count = api._make_path(path)
        print("Path:{0} count:{1}".format(path, count))
        # self.assertEqual(count, 3)

        path = "data/serial/0/mode"
        count = api._make_path(path)
        print("Path:{0} count:{1}".format(path, count))
        # self.assertEqual(count, 0)

        path = "data/serial/0/mode/"
        count = api._make_path(path)
        print("Path:{0} count:{1}".format(path, count))
        # self.assertEqual(count, 1)
        return


def do_template(self):
        pass


def do_object():

    api = cp_api.ApiRouterDisk()

    print('')
    path = "/"
    data = api.get(path)
    print("path({0}) = {1}".format(path, data))

    print('')
    path = "/config/serial"
    data = api.get(path)
    print("path({0}) = {1}".format(path, data))

    print('')
    path = "/config/serial/0"
    data = api.get(path)
    print("path({0}) = {1}".format(path, data))

    print('')
    path = "/config/serial/0/mode"
    data = api.get(path)
    print("path({0}) = {1}".format(path, data))

    print('')
    path = "/config/serial/0/mode"
    value = "tcp"
    data = api.put(path, value)
    print("put({0}, {1}) = {2}".format(path, value, data))

    print('')
    path = "/config/serial/0/port"
    value = 2101
    data = api.put(path, value)
    print("put({0}, {1}) = {2}".format(path, value, data))

    print('')
    path = "/config/serial/1/mode"
    value = "udp"
    data = api.put(path, value)
    print("put({0}, {1}) = {2}".format(path, value, data))

    print('')
    path = "/config/serial/1/port"
    value = 2001
    data = api.put(path, value)
    print("put({0}, {1}) = {2}".format(path, value, data))

    # tests = [
    #     {'cmd': 0x00, 'data': b'\x68\x1A', 'result': 65.0},
    #     {'cmd': 0x01, 'data': b'\x2E\xE0', 'result': 3000.0},
    # ]
    #
    # for test in tests:
    #
    #     value, uom, quality = _parse_parameter_data(test['cmd'], test['data'])
    #     _print(repr(test))
    #
    #     expect = test['result']
    #     if abs(value - expect) > 0.001:
    #         _logger.error('output_channel_name not as expected in %s', test)
    #         _logger.error('  value: %s', value)
    #         _logger.error(' expect: %s', expect)
    #         return False

    return True

if __name__ == '__main__':

    if False:
        unittest.main()

    else:
        # do_object()
        do_template()
