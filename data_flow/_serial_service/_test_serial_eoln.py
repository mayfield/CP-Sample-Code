__author__ = 'Lynn'

import logging
import sys

import serial_eoln


def test_object():

    obj = serial_eoln.Eoln()

    obj.set_mode('\r')
    logger.info('serial_eoln.mode = {0}'.format(obj.mode))

    tests = [
        {'input': b"", 'expect': [], 'complete': False},
        {'input': b"Hello", 'expect': ["Hello"], 'complete': False},
        {'input': b"Hello\r", 'expect': ["Hello\r"], 'complete': True},
        {'input': b"Hello\n", 'expect': ["Hello"], 'complete': False},
        {'input': b"Hello\r\n", 'expect': ["Hello\r"], 'complete': True},
        {'input': b"Hello\rcat", 'expect': ["Hello\r", "cat"], 'complete': False},
        {'input': b"Hello\ncat", 'expect': ["Hellocat"], 'complete': False},
        {'input': b"Hello\r\ncat", 'expect': ["Hello\r", "cat"], 'complete': False},
    ]

    for test in tests:
        assert isinstance(test, dict)

        result, complete = obj.process(test['input'])
        expect = test['expect']
        if result != expect:
            logger.error('serial_eoln.process({0}) not as expected'.format(test['input']))
            logger.error(' result:[{0}]'.format(result))
            logger.error(' expect:[{0}]'.format(expect))
            return False
        logger.debug('serial_eoln.process({0}) returned {1}'.format(test['input'], result))

        if complete != test['complete']:
            logger.error('serial_eoln.process({0}) complete wrong, saw {1} expected {2}'.format(
                test['input'], complete, test['complete']))
            return False

    obj.set_mode('\n')
    logger.info('serial_eoln.mode = {0}'.format(obj.mode))

    tests = [
        {'input': b"", 'expect': [], 'complete': False},
        {'input': b"Hello", 'expect': ["Hello"], 'complete': False},
        {'input': b"Hello\r", 'expect': ["Hello"], 'complete': False},
        {'input': b"Hello\n", 'expect': ["Hello\n"], 'complete': True},
        {'input': b"Hello\r\n", 'expect': ["Hello\n"], 'complete': True},
        {'input': b"Hello\ncat", 'expect': ["Hello\n", "cat"], 'complete': False},
        {'input': b"Hello\rcat", 'expect': ["Hellocat"], 'complete': False},
        {'input': b"Hello\r\ncat", 'expect': ["Hello\n", "cat"], 'complete': False},
    ]

    for test in tests:
        assert isinstance(test, dict)

        result, complete = obj.process(test['input'])
        expect = test['expect']
        if result != expect:
            logger.error('serial_eoln.process({0}) not as expected'.format(test['input']))
            logger.error(' result:[{0}]'.format(result))
            logger.error(' expect:[{0}]'.format(expect))
            return False
        logger.debug('serial_eoln.process({0}) returned {1}'.format(test['input'], result))

        if complete != test['complete']:
            logger.error('serial_eoln.process({0}) complete wrong, saw {1} expected {2}'.format(
                test['input'], complete, test['complete']))
            return False

    obj.set_mode('\r\n')
    logger.info('serial_eoln.mode = {0}'.format(obj.mode))

    tests = [
        {'input': b"", 'expect': [], 'complete': False},
        {'input': b"Hello", 'expect': ["Hello"], 'complete': False},
        {'input': b"Hello\r", 'expect': ["Hello\r\n"], 'complete': True},
        {'input': b"Hello\r\n", 'expect': ["Hello\r\n"], 'complete': True},
        {'input': b"Hello\ncat", 'expect': ["Hellocat"], 'complete': False},
        {'input': b"Hello\rcat", 'expect': ["Hellocat"], 'complete': False},
        {'input': b"Hello\r\ncat", 'expect': ["Hello\r\n", "cat"], 'complete': False},
    ]

    for test in tests:
        assert isinstance(test, dict)

        result, complete = obj.process(test['input'])
        expect = test['expect']
        if result != expect:
            logger.error('serial_eoln.process({0}) not as expected'.format(test['input']))
            logger.error(' result:[{0}]'.format(result))
            logger.error(' expect:[{0}]'.format(expect))
            return False
        logger.debug('serial_eoln.process({0}) returned {1}'.format(test['input'], result))

        if complete != test['complete']:
            logger.error('serial_eoln.process({0}) complete wrong, saw {1} expected {2}'.format(
                test['input'], complete, test['complete']))
            return False

    obj.set_mode(None)
    logger.info('serial_eoln.mode = {0}'.format(obj.mode))
    # there is no 'complete' test - is always False for RAW

    tests = [
        {'input': b"", 'expect': b""},
        {'input': b"Hello", 'expect': b"Hello"},
        {'input': b"Hello\r", 'expect': b"Hello\r"},
        {'input': b"Hello\r\n", 'expect': b"Hello\r\n"},
        {'input': b"Hello\ncat", 'expect': b"Hello\ncat"},
        {'input': b"Hello\rcat", 'expect': b"Hello\rcat"},
        {'input': b"Hello\r\ncat", 'expect': b"Hello\r\ncat"},
    ]

    for test in tests:
        assert isinstance(test, dict)

        result, complete = obj.process(test['input'])
        expect = test['expect']
        if result != expect:
            logger.error('serial_eoln.process({0}) not as expected'.format(test['input']))
            logger.error(' result:[{0}]'.format(result))
            logger.error(' expect:[{0}]'.format(expect))
            return False
        logger.debug('serial_eoln.process({0}) returned {1}'.format(test['input'], result))

    logger.info('   ... was Okay')
    logger.info(' ')
    return True


if __name__ == '__main__':
    global logger

    logger = logging.getLogger('test')
    logging.basicConfig()

    logger.setLevel(logging.INFO)
    # _logger.setLevel(logging.DEBUG)

    test_all = False
    if test_all:
        logger.setLevel(logging.INFO)

    if True or test_all:
        if not test_object():
            logger.error('TEST FAILED!')
            sys.exit(-1)
