__author__ = 'Lynn'

import logging
import sys
import time

import serial_hw


def test_object():

    obj = serial_hw.SerialHardware(0)
    obj.set_logger(logger)
    obj.open()

    message = b'Hello\r\n'
    now = time.time()
    count = obj.write(message, now)

    while True:
        now = time.time()
        obj.read(now)
        obj.tick(now)

        logger.debug("Tick %s" % time.strftime("%H:%M:%S", time.localtime()))
        time.sleep(1.0)

    obj.close()

    logger.info('   ... was Okay')
    logger.info(' ')
    return True


if __name__ == '__main__':
    global logger

    logger = logging.getLogger('test')
    logging.basicConfig()

    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    test_all = False
    if test_all:
        logger.setLevel(logging.INFO)

    if True or test_all:
        if not test_object():
            logger.error('TEST FAILED!')
            sys.exit(-1)
