# File: buffer.py
# Desc: collect data for a message buffer

import time


__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Dec Lynn
#       * initial draft
#


class MessageBuffer(object):
    """
    One data object, likely 'coalesced' over time until an Ond-of-message condition is true

    """

    BUFFER_COMPLETE = 'done'
    BUFFER_WAITING = 'wait'

    def __init__(self, ttl):
        """
        Add the original request, before client sends

        :param ttl: the raw seconds that this buffer must complete
        :type ttl: bytes
        """
        self.first_date = 0
        self.ttl = ttl
        self.data = None

        return

    @staticmethod
    def code_name():
        return 'MessageBuffer'

    @staticmethod
    def code_version():
        return __version__

    def reset(self):
        self.first_date = 0
        self.data = None
        return

    # def __repr__(self):
    #     """
    #     this is either:
    #     - if single, a name like "coral"
    #     - if double, is a string of tuple, such as "(white,black)"
    #     :return:
    #     """
    #     return str(self.name)

    def append(self, raw):
        """
        Add the original request, before client sends

        :param raw: the raw protocol packet
        :type raw: bytes
        :rtype: None
        """
        assert isinstance(raw, bytes)

        now = time.time()

        if self.first_date == 0:
            self.first_date = now
            self.data = raw

        else:
            self.data += raw
            if (now - self.first_date) > self.ttl:


        return len(self.data)
