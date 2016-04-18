# File: handler_tcp.py
# Desc: handler for a message packets from TCP/IP

# import queue
import json
import socket
import select
from threading import Thread
from packets.handler import PacketHandler


__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Nov Lynn
#       * initial draft
#


class TcpServer(PacketHandler):
    """
    Create a TCP Server instance (without thread).

    """
    DEF_IP_PORT = 10001
    DEF_BUF_SIZE = 1024
    DEF_SEL_TOUT = 5.0
    DEF_CLIENT_MAX = 3

    def __init__(self, name, mode=None):
        """
        :param name: a name for this handler
        :type name: str
        """
        super().__init__(name, mode)

        self.media = None

        self.buf_size = self.DEF_BUF_SIZE

        return

    @staticmethod
    def code_name():
        return 'TcpServer'

    def open(self, params=None):
        """
        Open our media

        :param params: any parameters
        :type params: None or dict or str
        :rtype: bool
        """
        super().open(params)

        self.import_params(params)

        self.media = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.media.bind((self.ip_bind_address, self.ip_port))
        return True

    # def is_open(self):

    def close(self):
        """
        Close our media

        :rtype: None
        """
        super().close()

        try:
            self.media.shutdown(socket.SHUT_RD)
            self.media.close()
        except socket.error:
            pass
        self.media = None

        return

    # def close_event(self):

    # def flush(self):

    def read(self, params=None):
        """
        Add the original request, before client sends

        :param params: any 'other' values
        :type params: None or dict
        :rtype: None or bytes
        """
        super().read(params)
        result = self.media.recv(self.buf_size)
        return result

    def write(self, data, params=None):
        """
        Add the original request, before client sends

        :param data: the raw protocol packet
        :type data: bytes
        :param params: any 'other' values
        :type params: None or dict
        :rtype: int
        """
        super().write(data, params)
        result = self.media.recv(data)
        return result

    def import_params(self, value):
        """
        Parse the TCP parameters, which can be either a python dict of JSON

        :param value: the source value as string
        :type value: dict or str
        :return: the string to use as the mode value
        :rtype: str
        """
        if value is None:
            return ""

        if isinstance(value, str):
            value = json.loads(value)

        if 'buf_size' in value:
            # parse the TCP recv buffer size
            self.buf_size = value['buf_size']
            self.logger.debug('Recv Buffer Size %d bytes' % self.buf_size)
        # else we leave it as is, likely self.DEF_BUF_SIZE

        # raise ValueError("Handler MODE must be set('srv', 'cli', 'peer')")


class TcpServerThread(Thread, TcpServer):
    """

    """
    DEF_IP_PORT = 10001
    DEF_BUF_SIZE = 1024
    DEF_SEL_TOUT = 5.0
    DEF_CLIENT_MAX = 3

    def __init__(self, name, mode=None):
        """
        :param name: a name for this handler
        :type name: str
        """
        TcpServer.__init__(self, name, mode)
        Thread.__init__(self, name=name)

        self.ip_port = self.DEF_IP_PORT
        self.ip_bind_address = socket.gethostname()
        self.sel_timeout = self.DEF_SEL_TOUT
        self.client_max = self.DEF_CLIENT_MAX

        self.r_list = []
        self.w_list = []
        self.x_list = []

        return

    @staticmethod
    def code_name():
        return 'TcpServerThread'

    def open(self, params=None):
        """
        Open our media

        :param params: any parameters
        :type params: None or dict or str
        :rtype: bool
        """
        self.import_params(params)

        self.media = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.media.bind((self.ip_bind_address, self.ip_port))
        return True

    # def is_open(self):

    def close(self):
        """
        Close our media

        :rtype: None
        """
        self.logger.debug('TCP Handler closing clients')
        if self.r_list is not None:
            assert isinstance(self.r_list, list)
            try:
                for sock in self.r_list:
                    sock.close()
            except socket.error:
                pass
        self.r_list = None
        self.media = None

        return

    # def close_event(self):

    # def flush(self):

    # def read(self, params=None):

    # def write(self, data, params=None):

    def start(self):
        """
        :return:
        """
        if self.state != self.STATE_OPEN:
            # bind and wait
            self.open()
        return

    def run(self):
        """
        :return:
        """
        self.r_list = [self.media]
        # self.w_list = [] and self.x_list = []
        try:
            while True:
                r_ready, w_ready, x_ready = select.select(
                    self.r_list, self.w_list, self.x_list, self.sel_timeout)

                for sock in r_ready:
                    if sock == self.media:
                        # accept a client
                        client, address = self.media.accept()
                        if len(self.r_list) > self.client_max:
                            self.logger.warning('Reject client(%s), too many' % address)
                            client.close()
                        else:
                            self.logger.warning('Accept client(%s)' % address)
                            self.r_list.append(client)

                    else:
                        # is incoming packet
                        self.logger.warning('Incoming Data')

        finally:
            self.logger.error('TCP Handler Shutting down')
            for sock in self.r_list:
                sock.close()
        return

    def import_params(self, value):
        """
        Parse the TCP parameters, which can be either a python dict of JSON

        :param value: the source value as string
        :type value: dict or str
        :return: the string to use as the mode value
        :rtype: str
        """
        if value is None:
            return ""

        if isinstance(value, str):
            value = json.loads(value)

        TcpServer.import_params(self, value)

        if 'ip_port' in value:
            # parse the TCP port value
            self.ip_port = value['ip_port']
            self.logger.debug('IP Port set to %d' % self.ip_port)
        # else we leave it as is, likely self.DEF_IP_PORT

        if 'sel_timeout' in value:
            # parse the TCP recv buffer size
            self.sel_timeout = value['buf_size']
            self.logger.debug('Select Timeout = %d sec' % self.sel_timeout)
        # else we leave it as is, likely self.DEF_SEL_TOUT

        if 'client_max' in value:
            # parse the TCP recv buffer size
            self.client_max = value['client_max']
            self.logger.debug('Max Clients = %d' % self.client_max)
        # else we leave it as is, likely self.DEF_CLIENT_MAX

        # raise ValueError("Handler MODE must be set('srv', 'cli', 'peer')")
