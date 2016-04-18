# File: handler_tcp_server.py
# Desc: handler for a message packets from TCP/IP

# import queue
import json
import socket
import select
from threading import Thread, Event
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
    DEF_BUF_SIZE = 1024

    def __init__(self, name, mode=None):
        """
        :param name: a name for this handler
        :type name: str
        """
        super().__init__(name, mode)

        self.media = None

        self.buf_size = self.DEF_BUF_SIZE

        self.logger.debug("TcpServer.init okay")
        return

    @staticmethod
    def code_name():
        return 'TcpServer'

    def set_media(self, sock):
        """
        Open our media

        :param sock: any parameters
        :type sock: None or dict or str
        :rtype: bool
        """
        super().open()

        self.media = sock

        self.logger.debug("TCPServer.Open")
        return True

    # def is_open(self):

    def close(self):
        """
        Close our media

        :rtype: None
        """
        super().close()

        if self.media is not None:
            try:
                self.media.shutdown(socket.SHUT_RD)
                self.media.close()
            except socket.error:
                pass
            self.media = None

        self.logger.debug("TCPServer.Close")
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
        result = self.media.write(data, params)
        return result

    def import_params(self, value):
        """
        Parse the TCP parameters, which can be either a python dict of JSON

        :param value: the source value as string
        :type value: dict or str
        :return: the string to use as the mode value
        :rtype: str
        """
        if value is None or len(value) == 0:
            return ""

        if isinstance(value, str):
            value = json.loads(value)

        if 'buf_size' in value:
            # parse the TCP recv buffer size
            self.buf_size = value['buf_size']
            self.logger.debug('Recv Buffer Size %d bytes' % self.buf_size)
        # else we leave it as is, likely self.DEF_BUF_SIZE

        # raise ValueError("Handler MODE must be set('srv', 'cli', 'peer')")


class TcpServerThread(Thread, PacketHandler):
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
        Thread.__init__(self, name=name)
        PacketHandler.__init__(self, name, 'srv')

        self.ip_port = self.DEF_IP_PORT
        # self.ip_bind_address = socket.gethostname()
        self.ip_bind_address = "127.0.0.1"
        self.sel_timeout = self.DEF_SEL_TOUT
        self.client_max = self.DEF_CLIENT_MAX

        self.listener = None

        self.keep_running = Event()
        self.keep_running.set()

        self.r_list = []
        self.w_list = []
        self.x_list = []

        self.client_dict = {}

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
        if params is not None:
            self.import_params(params)

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((self.ip_bind_address, self.ip_port))
        self.listener.listen(self.client_max + 1)

        self.logger.debug("TcpServerThread.Open(%s:%d)" % (self.ip_bind_address, self.ip_port))
        return True

    # def is_open(self):

    def close(self):
        """
        Close our media

        :rtype: None
        """
        self.logger.debug('TCP Handler closing clients')
        try:
            for sock in self.r_list:
                sock.close()
        except socket.error:
            pass
        self.r_list = []

        # the above loop should have also closed this listener, as it was r_list[0]
        self.listener = None

        self.keep_running.clear()

        self.state = self.STATE_IDLE
        self.logger.debug("TcpServerThread.Close")
        return

    # def close_event(self):

    # def flush(self):

    # def read(self, params=None):

    # def write(self, data, params=None):

    def start_server(self):
        """
        :return:
        """
        if self.state != self.STATE_OPEN:
            # bind and wait
            self.open()
        self.logger.debug("TcpServerThread.Start")

        self.daemon = True
        self.start()
        return

    def stop_server(self):
        """
        :return:
        """
        self.close()
        self.logger.debug("TcpServerThread.Stop")
        return

    def run(self):
        """
        :return:
        """
        self.logger.debug("TcpServerThread.Run")
        assert self.listener is not None
        self.r_list = [self.listener]
        # self.w_list = [] and self.x_list = []
        try:
            while self.keep_running.is_set():

                r_ready, w_ready, x_ready = select.select(
                    self.r_list, self.w_list, self.x_list, self.sel_timeout)
                self.logger.debug("TcpServerThread.Tick ...")

                for sock in r_ready:
                    if sock == self.listener:
                        # accept a client
                        # assert isinstance(self.listener, socket.socket)
                        client_sock, address = self.listener.accept()
                        if len(self.r_list) > self.client_max:
                            self.logger.warning('Reject client(%s), too many' % address)
                            client_sock.close()
                        else:
                            self.logger.info('Accept client(%s)' % str(address))
                            client_han = TcpServer(address[0], 'srv')
                            client_han.set_media(client_sock)
                            self.client_dict[client_sock] = client_han

                            self.r_list.append(client_sock)

                    else:
                        # is incoming packet
                        if sock in self.client_dict:
                            # then we have this client
                            client_han = self.client_dict[sock]
                            assert isinstance(client_han, TcpServer)
                            data = client_han.read()
                            self.logger.debug('Incoming Data, len()=%d' % len(data))

                        else:
                            self.logger.warning('unexpected data!')
                            sock.close()
                            self.r_list.remove(sock)

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
        if value is None or len(value) == 0:
            return ""

        if isinstance(value, str):
            value = json.loads(value)

        # PacketHandler.import_params(self, value)

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
