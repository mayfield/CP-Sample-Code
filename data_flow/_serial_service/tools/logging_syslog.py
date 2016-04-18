import logging
import logging.handlers
import sys
import time


def test_object():
    global logger

    while True:
        logger.debug("Tick %s" % time.strftime("%H:%M:%S", time.localtime()))
        time.sleep(15.0)

    logger.info('   ... was Okay')
    logger.info(' ')
    return True


if __name__ == '__main__':
    global logger

    logger = logging.getLogger('test')
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

    test_all = True

    if True or test_all:
        if not test_object():
            logger.error('TEST FAILED!')
            sys.exit(-1)
