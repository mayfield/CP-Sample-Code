# File: packet.py
# Desc: handler for a message packet

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Nov Lynn
#       * initial draft
#


class MessagePacket(object):
    """
    One packet to be handled

    self.state = (str) the state of the transaction
    self.req = (dict) original request, before client sends
    self.ind = (dict) received request, after server receives
    self.rsp = (dict) original response, before server sends
    self.con = (dict) received response, after client receives

    ['raw'] = (bytes) raw protocol packet
    ['dst'] = (?) server 'id'
    ['src'] = (?) client 'id'
    ['ttl'] = (float) time.time() after which packet is to be abandoned
    """

    STATE_IDLE = 'idle'
    STATE_QUEUED = 'que'
    STATE_WAITING = 'wait'
    STATE_GOOD = 'good'
    STATE_ABORT = 'abort'
    STATE_ERROR = 'error'

    TAG_RAW = 'raw'
    TAG_DST = 'dst'
    TAG_SRC = 'src'
    TAG_DEADLINE = 'ttl'

    def __init__(self):
        self.state = self.STATE_IDLE

        self.req = None
        self.ind = None
        self.rsp = None
        self.con = None
        self.params = None

        return

    @staticmethod
    def code_name():
        return 'MessagePacket'

    @staticmethod
    def code_version():
        return __version__

    def reset(self):
        self.state = self.STATE_IDLE
        self.req = None
        self.ind = None
        self.rsp = None
        self.con = None
        self.params = None
        return

    # def __repr__(self):
    #     """
    #     this is either:
    #     - if single, a name like "coral"
    #     - if double, is a string of tuple, such as "(white,black)"
    #     :return:
    #     """
    #     return str(self.name)

    def add_req(self, raw, params):
        """
        Add the original request, before client sends

        :param raw: the raw protocol packet
        :type raw: bytes
        :param params: any 'other' values
        :type raw: None or dict
        :rtype: None
        """
        assert isinstance(raw, bytes)
        assert len(raw) > 0

        self.reset()
        self.req = dict()
        self.req[self.TAG_RAW] = raw
        if params is not None:
            self.params = params
        return

    def queue_rsp(self, raw, params):
        """
        Prepare to send the request

        :param raw: the raw protocol packet
        :type raw: bytes
        :param params: any 'other' values
        :type raw: None or dict
        :rtype: None
        """
        assert isinstance(raw, bytes)
        assert len(raw) > 0

        self.reset()
        self.req = dict()
        self.req[self.TAG_RAW] = raw
        if params is not None:
            self.params = params
        return

    # self.ind = (dict) received request, after server receives
    # self.rsp = (dict) original response, before server sends
    # self.con = (dict) received response, after client receives
