from cp_lib.app_base import CradlepointAppBase
from simple.csclient.test_csclient import test_csclient


class RouterApp(CradlepointAppBase):

    def __init__(self, app_main):
        """
        :param str app_main: the file name, such as "network.tcp_echo"
        :return:
        """
        CradlepointAppBase.__init__(self, app_main)
        return

    def run(self):
        self.logger.debug("__init__ chaining to test_csclient()")

        # we do this wrap to dump any Python exception traceback out to Syslog
        try:
            result = test_csclient(self.logger, self.settings)
        except:
            self.logger.exception("CradlepointAppBase failed")
            raise

        return result
