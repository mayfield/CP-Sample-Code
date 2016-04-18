# File: stats.py
# Desc: the stats of a packet handler

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Nov Lynn
#       * initial draft
#


class HandlerStatistics(object):
    """
    hold the handler statistics, in-vs-out is per 'wire' perspective

    self.in_packets = (int) total packets received
    self.in_bytes = (int) total bytes received
    self.in_fragments = (int) total partial packets (might be 0)
    self.in_abort = (int) total discarded packets due to an error or timeout

    self.out_packets = (int) total packets sent
    self.out_bytes = (int) total bytes sent
    """

    def __init__(self):
        self.in_packets = 0
        self.in_bytes = 0
        self.in_fragments = 0
        self.in_abort = 0
        self.out_packets = 0
        self.out_bytes = 0
        return

    @staticmethod
    def code_name():
        return 'HandlerStatistics'

    @staticmethod
    def code_version():
        return __version__

    def reset(self):
        self.in_packets = 0
        self.in_bytes = 0
        self.in_fragments = 0
        self.in_abort = 0
        self.out_packets = 0
        self.out_bytes = 0
        return

    def __repr__(self):
        """
        this is either:
        - if single, a name like "coral"
        - if double, is a string of tuple, such as "(white,black)"
        :return:
        """
        return '{"class_type": %d, ' % self.code_name() +\
               ' "in_packets": %d,' % self.in_packets +\
               ' "in_bytes": %d,' % self.in_bytes +\
               ' "in_fragments": %d,' % self.in_fragments +\
               ' "in_abort": %d,' % self.in_abort +\
               ' "out_packets": %d,' % self.out_packets +\
               ' "out_bytes": %d}' % self.out_bytes

    def incr_packets_in(self, value=1):
        """
        Increment the total packets received

        :param value: the number of packets to add, default = 1
        :type value: int
        """
        self.in_packets += value
        return

    def incr_bytes_in(self, value):
        """
        Increment the total bytes received

        :param value: the number of bytes to add, NO default
        :type value: int
        """
        self.in_bytes += value
        return

    def incr_fragments_in(self, value=1):
        """
        Increment the total fragments received

        :param value: the number of fragments to add, default = 1
        :type value: int
        """
        self.in_fragments += value
        return

    def incr_abort_in(self, value=1):
        """
        Increment the total aborted/discarded packets due to an error or timeout

        :param value: the number of fragments to add, default = 1
        :type value: int
        """
        self.in_fragments += value
        return

    def incr_packets_out(self, value=1):
        """
        Increment the total packets sent

        :param value: the number of packets to add, default = 1
        :type value: int
        """
        self.out_packets += value
        return

    def incr_bytes_out(self, value):
        """
        Increment the total bytes sent

        :param value: the number of bytes to add, NO default
        :type value: int
        """
        self.out_bytes += value
        return
