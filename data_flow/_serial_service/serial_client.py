__author__ = 'Lynn'

import socket
import json

import serial_settings
import json_utility
# from serial_eoln import Eoln
from serial_buffer import SerialBuffer


class Client(object):

    def __init__(self):
        self._settings = serial_settings.SerialSettings()

        # hold the last data time (as seen by the Ip network)
        self.last_data_recv_time = 0
        self.last_data_proc_time = 0
        self.last_data_send_time = 0

        # hold data for a period
        self._recv_buffer = SerialBuffer()

        # some simple stats
        self.send_transactions = 0
        self.send_bytes = 0
        self.recv_errors = 0

        self._parent = None
        self.connection = None
        self.address = None
        self.recv_size = 1024
        self.send_size = 1024

        self._logger = None
        return

    def set_logger(self, logger):
        self._logger = logger
        self._recv_buffer.set_logger(logger)

    def set_parent(self, parent):
        self._parent = parent

    def close(self):
        """
        Do some simple clean up - perhaps speed garbage collection
        :return:
        """
        self.connection = None
        self.address = None
        self._logger = None
        return

    def tick(self, now):
        """
        A time-based 'tick' by a parent
        :param now:
        :type now: float
        :return:
        """
        return None

    def receive(self, now):
        """
        Assume have data, so receive it

        :param now: current ime
        :type now: float
        :return: None if error, else any data seen
        """
        try:
            data = self.connection.recv(self.recv_size)
            if not data:
                # peer likely hung up!
                self._logger.debug("Client gone offline")
                return None

            else:  # echo back the client message
                if self._logger is not None:
                    self._logger.debug("See Data[{}]".format(data))

                # time-stamp the receive
                self.last_data_recv_time = now

        except socket.error:
            if self._logger is not None:
                self._logger.debug("Client gone offline")
            # signal our closing
            return None

        return data

    def process(self, now):
        """
        handle the data in the buffer

        :param now: current ime
        :type now: float
        :return:
        """
        if self._logger is not None:
            self._logger.debug("Process data")

        self.last_data_proc_time = now

        self.send(now, self._recv_buffer)
        self._recv_buffer = None
        return

    def send(self, now, data=None):
        """
        handle the data in the buffer

        :param now: current time
        :type now: float
        :param data:
        :type data: str or bytes or None
        :return:
        """
        if data is None:
            # then see about our _recv_buffer
            data = self._recv_buffer

        self.last_data_send_time = now

        count = self.connection.send(data.encode())
        return count

    def get_report(self):
        """
        :return:
        """
        result = dict()
        result['name'] = "{0}.{1}".format(self.address[0], self.address[1])
        result['status'] = "active"
        return result


class ControlClient(Client):
    """
    A Control Client sends in JSONRPC commands. The incoming is assumed ASCII JSON, and also that each request
    is a single TCP segment.
    """

    # TODO - consider how to handle fragmented JSON?

    JSONRPC_VERSION = "2.0"

    def __init__(self):
        super().__init__()

        # these 2 arne't used?
        self.recv_bytes = None
        self.send_bytes = None
        return

    # def close(self): - use parent

    # def tick(self, now): - use super class

    def receive(self, now):
        """
        Assume have data, so receive it

        :param now: current time
        :type now: float
        :return: True if okay, else False to close this client
        """

        # let our super-class receive
        data = super().receive(now)
        if data is None:
            # then no data, so error or hanging up
            return False

        # convert the bytes to JSON ASCII
        assert isinstance(data, bytes)
        data = data.decode()
        try:
            data = json.loads(data)
            self.recv_transactions += 1

        except ValueError as err:
            # something very wrong - hangup
            self.recv_errors += 1
            if self._logger is not None:
                self._logger.error(err)
            return False

        if "jsonrpc" not in data or data["jsonrpc"] != self.JSONRPC_VERSION:
            if self._logger is not None:
                self._logger.error("Bad JSON RPC seen")
            self.recv_errors += 1
            result = json_utility.make_json_error(json_utility.JSONRPC_INVALID_REQUEST, identifier=data.get("id", None))
            self.send(now, result)
            return True

        if data["method"] == "echo":
            result = self.do_echo(data)
            self.send(now, result)

        elif data["method"] == "open":
            result = self.do_open(data)
            self.send(now, result)

        elif data["method"] == "report":
            result = self.do_report(data)
            self.send(now, result)

        else:
            if self._logger is not None:
                self._logger.error("JSONRPC Method Not Found")
            self.recv_errors += 1
            result = json_utility.make_json_error(json_utility.JSONRPC_METHOD_NOT_FOUND,
                                                  identifier=data.get("id", None))
            self.send(now, result)
            return True

        # self.recv_transactions, self.send_transactions, self.recv_bytes, self.send_bytes, self.recv_errors

        return True

    def process(self, now):
        """
        handle the data in the buffer

        :param now: current ime
        :type now: float
        :return:
        """
        if self._logger is not None:
            self._logger.debug("Process data")

        self.last_data_proc_time = now

        self.send(now, self._recv_buffer)
        self._recv_buffer = None
        return

    def send(self, now, data=None):
        """
        handle the data in the buffer

        :param now: current ime
        :type now: float
        :param data: the data to sned
        :type data: dict or str or bytes or None
        :return:
        """
        assert data is not None

        if isinstance(data, dict):
            data = json.dumps(data)

        self.send_transactions += 1
        return super().send(now, data)

    @staticmethod
    def do_echo(data):
        """
        handle the ECHO RPC call
        :param data: the parsed JSON
        :type data: dict
        :return:
        """
        if "params" in data:
            data["result"] = data["params"]

        else:
            data["result"] = True

        # flush out ["params"] and ["method"], assume ["jsonrpc"] and ["id"] as desired
        data = json_utility.clean_json_result(data)

        return data

    def do_open(self, data):
        """
        handle the OPEN RPC call (start a listener)

        :param data: the parsed JSON
        :type data: dict
        :return:
        """

        # To open a listener, we require these values:
        # ["ip_mode"] - open as TCP. UDP, etc.
        # ["ip_port"] - what IP port (2101, etc)
        # ["net_encode"] - how is the data packed? Encoded?
        if self._parent is None:
            data["result"] = None

        else:

            data["result"] = self._parent.get_report()

        # flush out ["params"] and ["method"], assume ["jsonrpc"] and ["id"] as desired
        data = json_utility.clean_json_result(data)

        return data

    def do_report(self, data):
        """
        handle the ECHO RPC call
        :param data: the parsed JSON
        :type data: dict
        :return:
        """
        if self._parent is None:
            data["result"] = None

        else:

            data["result"] = self._parent.get_report()

        # flush out ["params"] and ["method"], assume ["jsonrpc"] and ["id"] as desired
        data = json_utility.clean_json_result(data)

        return data


class SerialClient(Client):

    def __init__(self, index):
        super().__init__()

        # used to access the settings
        self.index = index

        # value = '\n'
        # if value is None:
        #     self.eoln = None
        # else:
        #     self.eoln = Eoln()
        #     self.eoln.set_mode(value)

        self.eoln = None

        return

    # def close(self): - use super()

    def tick(self, now):
        """
        A time-based 'tick' by a parent
        :param now:
        :type now: float
        :return:
        """
        if self._recv_buffer is None:
            return None

        return self._recv_buffer.tick(now)

    def receive(self, now):
        """
        Assume have data, so receive it

        :param now: current ime
        :type now: float
        :return:
        """
        data = super().receive(now)
        if data is None:
            # then no data, so error or hanging up
            return False

        # convert received bytes to desired form
        data = self._decoder(data)

        return True

    def process(self, now):
        """
        handle the data in the buffer

        :param now: current ime
        :type now: float
        :return:
        """
        if self._logger is not None:
            self._logger.debug("Process data")

        self.last_data_proc_time = now

        self.send(now, self._recv_buffer)
        self._recv_buffer = None
        return
