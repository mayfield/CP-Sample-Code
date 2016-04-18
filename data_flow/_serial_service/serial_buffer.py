__author__ = 'Lynn'

import copy

import serial_settings
import serial_encode


class SerialBuffer(object):

    """
    The SerialBuffer object helps defragment incoming data, and also does the object conversion/coding.

    Defrag is done via:
    - a user assigned 'end_of_message' detection function
    - by an idle time - after x seconds, assume is complete
    - option to include traditional EOLN (CR or NL) detection
    - to have the buffer hold "forever", set a hugely long idle/discard timeout & call get_data()

    For the 'conversion/coding', it handles the ZIP, hexascii, base64 (& so on) coding

    To use, when data is received, it is handed to the SerialBuffer instance. It returns any
    'complete' message, which have been decoded. If nothing is returned, that means more data is required

    To handle the idle-timeout, the user needs to 'tick' the buffer periodically.
    """

    DEF_IDLE_DISCARD = 300
    DEF_IDLE_PACK = 5

    def __init__(self):
        # hold data for a period, to allow defragmentation based on idle time
        self._recv_buffer = None

        # record the last new data time.time() - used for aging for pack/discard
        self.last_data_time = 0

        # in-coder is the 'decoder' - how we import data from wire (incoming or received)
        # out-coder is the 'encoder' - how we export data to wire (outgoing or transmitted)
        self._in_coder = serial_encode.from_net_binary
        self._out_coder = serial_encode.to_net_binary

        # time-outs, to pack/forward data (set to 0 to disable)
        self.recv_idle_pack_seconds = self.DEF_IDLE_PACK

        # time-outs, to 'discard' data (set to 0 to disable). Although recv_idle_discard_seconds
        # is normally larger than recv_idle_pack_seconds, if the self.tick() function is not called
        # for too long, then the DISCARD might take effect!
        self.recv_idle_discard_seconds = self.DEF_IDLE_DISCARD

        # hold basic stats
        self.total_wire_bytes_proc = 0  # bytes encoded (ZIP, etc)
        self.total_raw_bytes_proc = 0   # decoded bytes
        self.total_segments_proc = 0    # 'chunks' of data, maybe fragmented
        self.total_messages_proc = 0    # number of times a 'end-of-message' is detected
        # obviously, in SOME situations, total_wire_bytes_proc == total_raw_bytes_proc and
        # total_segments_proc == total_messages_proc

        # optional user function to test for end-of-message condition
        self.end_of_message = self.default_end_of_message

        # allow use of logging-like function during regression testing
        self._logger = None

        return

    def __len__(self):
        if self._recv_buffer is None:
            return 0
        else:
            return len(bytes(self._recv_buffer))

    def set_logger(self, logger):
        self._logger = logger

    def set_decoding(self, encode_mode: str):
        """
        Set the decoding - in py 3.x, sockets and pyserial expect bytes type (not str/unicode).
        However, the data might be ZIPPED, etc. This routine hides/abstracts this away from the
        client driver.

        :param encode_mode: encoding scheme to use (None means raw) see settings.NET_ENCODE_LIST
        :return:
        """
        if encode_mode is None or encode_mode == serial_settings.NET_ENCODE_BINARY:
            # special - skip any call (is fastest)
            self._in_coder = None
            self._out_coder = None

        else:
            self._in_coder = serial_encode.get_func_from_net(encode_mode)
            self._out_coder = serial_encode.get_func_to_net(encode_mode)

        return

    def set_end_of_message_callback(self, callback):
        """
        Add a protocol-specific 'callback' to test for end-of message

        :param callback:
        :return:
        """
        if callback is None:
            self.end_of_message = self.default_end_of_message

        else:
            if callback(callback):
                self.end_of_message = callback
            else:
                raise ValueError("end-of-message value must be callable()")
        return

    @staticmethod
    def default_end_of_message(data: bytes):
        """
        A dummy method, to allow better type checking in pycharm
        :param data:
        :return:
        :rtype: None or list, None or bytes
        """
        return None, data

    def reset(self):
        """
        Clear everything

        :return:
        """
        self._recv_buffer = None
        self.last_data_time = 0
        self.clear_statistics()
        return

    def clear_statistics(self):
        """
        Clear the totals by bytes, segments, etc

        :return:
        """
        self.total_wire_bytes_proc = 0
        self.total_raw_bytes_proc = 0
        self.total_segments_proc = 0
        self.total_messages_proc = 0
        return

    def data_get(self):
        """
        Manually get all the data, clearing the buffer and any EOM-states. The number of
        'messages' handled is also incremented by 1

        :return: the contents of recv_buffer, which is cleared
        :rtype: bytes
        """
        result = self._recv_buffer
        self._recv_buffer = None
        # increment the number of messages handled, which is by definition only 1
        self.total_messages_proc += 1
        return result

    def data_peek(self):
        """
        Get a COPY of all the data. Buffer and states are NOT affected.

        To work directly with the buffer, use obj._recv_buffer directly.

        :return: COPY of the contents of recv_buffer, which is NOT affected
        :rtype: bytes
        """
        return copy.copy(self._recv_buffer)

    def process(self, data: bytes, now: float):
        """
        converts the data to the correct form

        :param data: the raw data from wire (socket or pyserial)
        :param now: the current time.time()
        :return:
        :rtype: list or None
        """
        if data is None or len(data) == 0:
            # then no data passed in!
            return None

        self.total_wire_bytes_proc += len(data)
        self.last_data_time = now

        if self._in_coder is not None:
            # then do the decode - convert to raw bytes
            data = self._in_coder(data)

        self.total_raw_bytes_proc += len(data)
        self.total_segments_proc += 1

        if self._recv_buffer is None:
            # this is the FIRST data this period, and will be most common action
            self._recv_buffer = data

        else:  # else we have some pending data
            assert self.last_data_time != 0
            if self.recv_idle_discard_seconds and \
                    (now - self.last_data_time) > self.recv_idle_discard_seconds:
                # buffered data is too old, so discard; new data becomes everything
                if self._logger is not None:
                    self._logger.debug("Idle TOut - discard {0} bytes".format(len(self)))
                self._recv_buffer = data

            else:  # age is okay - crc_append new data to old
                self._recv_buffer += data

        if self.end_of_message != self.default_end_of_message:
            # test for protocol-specific end-of-message condition
            message_list, remainder = self.end_of_message(bytes(self._recv_buffer))
            if message_list is not None:
                # then we do have end-of-message, assume this is 'list' of 1 or more messages
                self._recv_buffer = remainder   # might be None, or extra data

                # incr the number of messages in list
                assert isinstance(message_list, list)
                self.total_messages_proc += len(message_list)
                return message_list
            # else, remainder == self._recv_buffer already, so just leave as is
            return None

        elif self.recv_idle_pack_seconds > 0:
            # we only check if we have an idle_pack timeout
            return self.tick(now)

        else:  # else assume caller wants this data; get and clear the recv_buffer
            return [self.data_get()]

    def tick(self, now: float):
        """
        A time-based 'tick' by a parent
        :param now:
        :return: None, or a list of 'messages'
        :rtype: list or None
        """
        if self._recv_buffer is None:
            # then nothing to do
            return None

        # Since recv_idle_discard_seconds is normally larger than recv_idle_pack_seconds,
        # we'll generally NEVER do the discard ... unless the self.tick() function has not been
        # called for too long, then the DISCARD might take effect!
        if self.recv_idle_discard_seconds > 0:
            # then we optionally discard data which is too old
            if (now - self.last_data_time) > self.recv_idle_discard_seconds:
                result = self._recv_buffer
                if self._logger is not None:
                    self._logger.debug("Idle TOut - discard {0} bytes".format(len(result)))
                self._recv_buffer = None
                return None

        if self.recv_idle_pack_seconds > 0:
            # then we pack and handle the pending data
            if (now - self.last_data_time) > self.recv_idle_pack_seconds:
                result = self.data_get()
                if self._logger is not None:
                    self._logger.debug("Idle TOut - pack and process {0} bytes".format(len(result)))
                return [result]

        return None

    def outgoing_encode(self, data: bytes):
        """
        A helper - allows a driver to 'defer' handling of the encoding method for TRANSMISSION
        to the SerialBuffer used for receiving, meaning the outbound data will match encoding
        (like ZIP, hexascii, etc)

        :param data: the data to send on wire
        :return:
        :rtype: bytes
        """
        if data is not None and self._out_coder is not None:
            # then do the decode - convert to raw bytes
            data = self._out_coder(data)
        return data
