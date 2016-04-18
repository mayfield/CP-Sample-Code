import logging
import socket
import struct
import time
import queue


class ImonnitUpload(object):

    IMONNIT_VERSION = b'\x02'

    MSG_TYPE_PUT_DATA = b'\x00\x00'
    MSG_TYPE_GET_ID_LIST = b'\x02\x00'

    # allows OEM to use a private 'pass code' - optional
    DEFAULT_SECURITY = b'\x00\x00\x00\x00'

    # 0x0000 means is line-powered, else is battery/solar info
    DEFAULT_POWER = b'\x00\x00'

    SEQ_NO_MIN = 0
    SEQ_NO_MAX = 0x7F

    UPLOAD_QUEUE_LIMIT = 1000

    def __init__(self):
        self.apn_id = 0
        self._apn_id_bytes = None
        self._seq_no = 0

        self._queue = queue.Queue()
        self.oldest_time = 0

        self.last_upload = 0
        self.saved_request = None
        self.saved_response = None
        return

    def get_queue_object(self):
        return self._queue

    def set_apn_id(self, value: int):
        """

        :param value:
        :return:
        """
        assert 0 < value < 0xFFFFFFF

        self.apn_id = value
        self._apn_id_bytes = struct.pack("<I", value)
        return

    def increment_seq_no(self, use=None, adder=1):
        """

        :param use: if an Int, then use this value
        :param adder:
        :return:
        """
        if use is not None:
            self._seq_no = use

        else:
            self._seq_no += adder

        if self._seq_no < self.SEQ_NO_MIN or self._seq_no > self.SEQ_NO_MAX:
            self._seq_no = self.SEQ_NO_MIN

        return

    def build_upload(self, force_time=None):
        """

        :param force_time: allow a 4-byte 'fake' upload time to pushed for testing
        :type force_time: bytes
        :return:
        :rtype: bytes
        """
        from monnit.utility import get_monnit_utc_le32
        result = self._build_header()

        # we'll do this a bit backwards - in case new messages get queued WHILE we build this
        # if we 'trust' qsize, it might change during build!
        count = 0
        payload = b''
        while True:
            try:
                payload += self._queue.get_nowait()
                count += 1

            except queue.Empty:
                # we have all of the messages
                break

        result += struct.pack("<H", count)
        logging.debug("iMonnit Upload - count = %d" % count)

        if count > 1:
            if force_time is None:
                force_time = get_monnit_utc_le32()
            else:
                assert isinstance(force_time, bytes)
                assert len(force_time) == 4
            result += force_time + payload
        # else if count == 0, then no TIME nor payload

        self.oldest_time = 0

        return result

    def _build_header(self):
        """

        :return:
        :rtype: bytes
        """
        # 64000000 00000000 02  00  0000  0000
        # APNID    Security Ver Seq Power MsgType
        assert self._apn_id_bytes is not None

        result = self._apn_id_bytes + self.DEFAULT_SECURITY + self.IMONNIT_VERSION
        result += bytes([self._seq_no])
        self.increment_seq_no()
        result += self.DEFAULT_POWER + self.MSG_TYPE_PUT_DATA

        return result

    def do_upload_or_heartbeat(self, now=None, save=False):
        """
        Do the actual upload. If count is zero, we consider this a 'heartbeat'

        :param now: time.time()
        :type now: float
        :param save: T/F if we want the upload data object 'saved', else is del'd
        :type save: bool
        :return:
        """
        from monnit.site_config import IMONNIT_HEARTBEAT

        if now is None:
            now = time.time()

        if self._queue.qsize():
            # upload if we have something to upload
            return self.do_upload(save)

        if now - self.last_upload > IMONNIT_HEARTBEAT:
            # then nothing, but still upload to refresh iMonnit health
            return self.do_upload(save)

        return False

    def do_upload(self, save=False):
        """
        Do the actual upload. If count is zero, we consider this a 'heartbeat'

        :param save: T/F if we want the upload data object 'saved', else is del'd
        :type save: bool
        :return:
        :rtype: bytes
        """
        from monnit.site_config import IMONNIT_HOSTNAME, IMONNIT_PORT

        logging.info("iMonnit Upload - begin, count = %d" % self._queue.qsize())

        # we confirm can connect FIRST, else leave data queued!
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IMONNIT_HOSTNAME, IMONNIT_PORT))
        except socket.error:
            logging.warning("iMonnit Upload - failed to connect!")
            return False

        # at this point, we are connected, so suck data from queue

        data = self.build_upload()
        # assert len(self.saved_request) > 0

        if save:
            self.saved_request = data
        else:
            self.saved_request = None
        self.saved_response = None

        self.last_upload = time.time()

        try:
            s.send(data)
            response = s.recv(4096)
            s.close()
            diff = time.time() - self.last_upload
            logging.debug("iMonnit Upload - successful, time=%0.2f sec" % diff)

        except socket.error:
            logging.warning("iMonnit Upload - failed to connect!")
            response = None

        if save:
            self.saved_response = response

        return response

    def queue_message(self, message):
        """
        Queue a message for iMonnit

        :param message: 1 message
        :type message: bytes
        :return:
        """
        if self._queue.qsize() > self.UPLOAD_QUEUE_LIMIT:
            # then too much old data!
            self._queue.get()
            logging.error("iMonnit Upload Q full - discard 1 old message")

        if self.oldest_time == 0:
            self.oldest_time = time.time()

        self._queue.put(message)
        logging.debug("iMonnit Upload - add 1 message, qsize = %d" % self._queue.qsize())
        return

    def queue_size(self):
        """
        :return: fetch the queue size
        :rtype: int
        """
        return self._queue.qsize()

    def queue_age(self):
        """
        :return: fetch the queue size
        :rtype: int
        """
        if self.oldest_time == 0:
            return 0.0
        else:
            return time.time() - self.oldest_time
