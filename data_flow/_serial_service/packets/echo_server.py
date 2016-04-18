# File: echo_server.py
# Desc: a simple handler, which merely echos what is queued for it

import queue
from packets.handler import PacketHandlerThread


__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Nov Lynn
#       * initial draft
#


class EchoServerHandler(PacketHandlerThread):
    """
    Link to a 'dealer', and any string queued, crc_append a string & return
    """

    def __init__(self, name, mode=None):
        """
        :param name: a name for this handler
        :type name: str
        """
        super().__init__(name, mode)
        return

    @staticmethod
    def code_name():
        return 'EchoServerHandler'

    def run(self):
        while True:
            try:
                data = self.queue_in.get(block=True, timeout=10.0)
                self.logger.debug("Data:%s" % data)
            except queue.Empty:
                self.logger.debug("Idle")
