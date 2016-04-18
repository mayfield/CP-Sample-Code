# File: handler.py
# Desc: handler for a message packet

import queue
import logging
from threading import Thread


__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Nov Lynn
#       * initial draft
#


class PacketHandlerIOError(IOError):
    pass


class PacketHandler(object):
    """
    A packet handler is the basic client/server module. It has the following basic function:
    1) requests/indications - protocol packets arrive on a media (ie: Ethernet or serial)
    2) some initial validation MIGHT occur (SOM/EOM symbols, checksum, length fields)
       2a) if validation fails, the data might be dropped, or an error returned
    3) if the packet is valid, a routing 'decision' might be made, selecting 1 of N destinations
       3a) if a destination is selected, the packet is queued, plus timeouts handled
       3b) if no destination is selected, the packet might be dropped, or an error returned
    4) the destination (, One packet to be handled

    Modes: (self.mode)
    MODE_SERVER/srv = we expect media packets, which we queue for 'destination'
    MODE_CLIENT/
    """

    STATE_IDLE = 'idle'
    STATE_OPEN = 'open'

    MODE_SERVER = 'srv'
    MODE_CLIENT = 'cli'
    MODE_PEER = 'peer'
    MODE_DEFAULT = 'peer'

    def __init__(self, name, mode=None):
        """
        :param name: a name for this handler
        :type name: str
        """
        if not isinstance(name, str):
            raise TypeError("Handler name must be type=str")
        self.name = name

        self.logger = logging.getLogger(name)
        # self.logger.setLevel(logging.INFO)

        self.state = self.STATE_IDLE

        # an exception is throw is mode is not value
        self.mode = self.validate_mode(mode)
        self.logger.debug("set to mode:%s" % self.mode)

        # things waiting for us from a PEER
        self.queue_in = queue.Queue()
        # if mode in (self.MODE_SERVER, self.MODE_PEER):
        #     # then we receive on media, Q for others, but expect incoming Queue
        #     self.queue_in = queue.Queue()
        return

    @staticmethod
    def code_name():
        return 'PacketHandler'

    @staticmethod
    def code_version():
        return __version__

    # def reset(self):
    #     self.state = self.STATE_IDLE
    #     self.req = None
    #     self.ind = None
    #     self.rsp = None
    #     self.con = None
    #     self.params = None
    #     return

    # def __repr__(self):
    #     """
    #     this is either:
    #     - if single, a name like "coral"
    #     - if double, is a string of tuple, such as "(white,black)"
    #     :return:
    #     """
    #     return str(self.name)

    def open(self, params=None):
        """
        Open our media

        :param params: any parameters
        :type params: None or dict or str
        :rtype: bool
        """
        if self.state == self.STATE_OPEN:
            self.close()
        if params:
            pass

        self.state = self.STATE_OPEN
        return True

    def is_open(self):
        """
        :return: T/F, if our media is open
        :rtype: bool
        """
        return self.state == self.STATE_OPEN

    def close(self):
        """
        Close our media

        :rtype: None
        """
        if self.state == self.STATE_OPEN:
            self.flush()
        self.logger.debug("CLOSE")
        self.state = self.STATE_IDLE
        return

    def close_event(self):
        """
        External peer/event asks us to close
        """
        self.logger.debug("CLOSE_EVENT")
        return self.close()

    def flush(self):
        """
        Discard any outstanding packets
        :rtype: None
        """
        self.logger.debug("FLUSH")
        while not self.queue_in.empty():
            self.queue_in.get()
        # TODO - flush any messages we've queued for peers
        return

    def read(self, params=None):
        """
        Add the original request, before client sends

        :param params: any 'other' values
        :type params: None or dict
        :rtype: None
        """
        if self.state != self.STATE_OPEN:
            raise PacketHandlerIOError("Media is not open")
        return None

    def write(self, data, params=None):
        """
        Add the original request, before client sends

        :param data: the raw protocol packet
        :type data: bytes
        :param params: any 'other' values
        :type params: None or dict
        :rtype: int
        """
        if self.state != self.STATE_OPEN:
            raise PacketHandlerIOError("Media is not open")
        return 0

    def validate_mode(self, value):
        """
        Given a 'mode', validate it, return the cooked value, or throw exception. source is
        not case sensitive.


        Input set ('pee', 'peer', 'ser', srv', 'cli')
        Output set ('peer', 'srv', 'cli')

        :param value: the source value as string
        :type value: None or str
        :return: the string to use as the mode value
        :rtype: str
        """
        if value is None:
            value = self.MODE_DEFAULT

        if not isinstance(value, str):
            raise TypeError("Handler MODE must be type string.")

        value = value.lower()
        if value in ('pee', self.MODE_PEER):
            return self.MODE_PEER
        elif value in ('srv', 'ser', self.MODE_SERVER):
            return self.MODE_SERVER
        elif value in ('cli', self.MODE_CLIENT):
            return self.MODE_CLIENT

        raise ValueError("Handler MODE must be set('srv', 'cli', 'peer')")


class PacketHandlerThread(Thread, PacketHandler):

    def __init__(self, name, mode=None):
        PacketHandler.__init__(self, name, mode)
        Thread.__init__(self, name=name)

    def start(self):
        """
        :return:
        """
        pass

    def run(self):
        """
        :return:
        """
        pass
