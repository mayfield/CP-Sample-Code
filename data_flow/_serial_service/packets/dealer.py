# File: dealer.py
# Desc: the dealer - distribute packets


from packets.packet import MessagePacket


__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Nov Lynn
#       * initial draft
#


class PacketDealer(object):
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
        return 'PacketDealer'

    @staticmethod
    def code_version():
        return __version__

    def deal(self, packet):
        """
        Deal the packet, or return in error

        :param packet: the message packet object
        :type packet: MessagePacket
        """
        assert isinstance(packet, MessagePacket)

        if 'dst' in packet.params:
            # then we have a destination
            pass

        else:
            pass
        return


class DealerTarget(object):
    """
    The object which tests/maps a destination to a target.

    Normally, a message packet includes a 'destination' (or ['dst']) value, which could be a
    simple integer (such as Modbus protocol slave address), an IP, or even a name.

    The target list is on of the following:
    1) if None, then ALL targets match this object
    2) if a list, then the [dst] must be in the list to match
    3) else the 'dst' must be a perfect match
    """

    def __init__(self):
        self.dst_list = None
        self.target = None

    def add_target_exact(self, target, dst_value):
        if isinstance(dst_value, list):
            raise ValueError("add_target_exact() needs exact value")
        return self._add_target(target, dst_value)

    def add_target_int_range(self, target, dst_value):
        if len(dst_value) != 2:
            raise ValueError("add_target_int_range() needs an integer value")
        if not isinstance(dst_value, int):
            raise ValueError("add_target_int_range() needs an integer value")
        return self._add_target(target, dst_value)

    def _add_target(self, target, dst_value):
        """
        Test if this packet goes to this target list

        :param target: the protocol object
        :type target: MessagePacket
        :param dst_value: optional target value
        """
        self.dst_list = dst_value

        if not isinstance(target, int):
            raise TypeError("invalid target type")

        self.target = target
        return

    def test_target(self, packet, dst=None):
        """
        Test if this packet goes to this target list

        :param packet: the message packet object
        :type packet: MessagePacket
        :param dst: optional target value
        """

        if self.dst_list is None:
            # then this is an else/any target
            return self.target

        if dst is not None:
            # caller did not pass in a specific target
            if 'dst' in packet.params:
                dst = packet.params['dst']

            else:
                raise ValueError("test_target requires a 'dst'/destination value")

        if dst == self.dst_list:
            # then is an exact match
            return self.target

        elif dst in self.dst_list:
                return self.target

        return None
