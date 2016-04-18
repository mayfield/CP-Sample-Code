__author__ = 'Lynn'

import logging
import socket
import ssl
import select
import time
import gc

from serial_settings import SerialSettings
from serial_object import SerialObject
from serial_client import Client, ControlClient, SerialClient

SELECT_TIMEOUT = 2.0
SOCKET_BUFFER_SIZE = 4096

# for now, control exists only on the localhost
CONTROL_LISTEN_ADDRESS = "localhost"

# serial should exist on "all" interfaces
SERIAL_LISTEN_ADDRESS = "0.0.0.0"


class ControlSocket(object):

    FORCE_TLS = True
    USE_TLS = ssl.PROTOCOL_TLSv1_1

    def __init__(self):
        self._settings = SerialSettings()

        self.max_port = self._settings.get_value("max_ports", None)
        self.serial_list = []

        # start by enabling the control socket on local-host

        # self._mode = self._settings.get_value("control_mode", 0)
        # if self._mode == "udp":
        #     self.socket_protocol = socket.SOCK_DGRAM
        # elif self._mode == "tls":
        #     self.socket_protocol = socket.SOCK_DGRAM
        # else:
        #     self.socket_protocol = socket.SOCK_STREAM
        #     self._mode = 'tcp'

        # for now, hard-code to TLS
        self._mode = "tls"
        self.socket_protocol = socket.SOCK_STREAM
        self.tls_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)

        self.ip_port = self._settings.get_value("control_port", None)

        self.select_timeout = SELECT_TIMEOUT

        # conn_list is the pure socket list for select()
        self._conn_list = []

        # client_list maps socket (as key) to Client object (in serial_client)
        self._client_list = {}

        # This is the 1 fixed listener for incoming control channels
        self.tls_control_listener = None

        # add the serial listners as a special collection; number matches the serial objects
        self.serial_listeners = []

        self.can_read = None
        self.can_write = None
        self.can_exec = None

        return

    def control_start(self):
        """
        Start the control socket, bind on correct interface, and so on
        """

        # start with the SSL context (was made up in __init__)
        # self.tls_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
        # certfile is the public info - including any CA chains
        # keyfile is the private key
        # self.tls_context.load_cert_chain(certfile="api/test.key")
        self.tls_context.load_cert_chain(certfile="api/cert.pem", keyfile="api/key.pem")

        # create an socket as appropriate form TCP or UDP - we have one fixed listener for CONTROL
        logger.debug("preparing to listen for mode:{0} on {1}:{2}".format(self._mode,
                                                                          CONTROL_LISTEN_ADDRESS, self.ip_port))
        self.tls_control_listener = socket.socket(socket.AF_INET, self.socket_protocol)
        self.tls_control_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tls_control_listener.bind((CONTROL_LISTEN_ADDRESS, self.ip_port))
        self.tls_control_listener.listen(5)

        self._conn_list = [self.tls_control_listener]
        self._client_list = {self.tls_control_listener: None}
        return

    def control_accept(self):
        """
        Start the control socket, bind on correct interface, and so on
        """
        connection, address = self.tls_control_listener.accept()
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        try:
            tls_socket = self.tls_context.wrap_socket(connection, server_side=True)
            self.add_control_client(tls_socket, address)
            return tls_socket, address

        except ssl.SSLError as err:
            logger.error("{0}".format(err))
            return None, None

    def serial_start(self):
        """
        Start one of N serial socket listeners, bind on correct interface, and so on
        """

        # create an socket as appropriate form TCP or UDP
        logger.debug("preparing to listen for mode:{0} on {1}:{2}".format(self._mode,
                                                                          SERIAL_LISTEN_ADDRESS, self.ip_port))
        serial_socket = socket.socket(socket.AF_INET, self.socket_protocol)
        serial_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serial_socket.bind((SERIAL_LISTEN_ADDRESS, self.ip_port))
        serial_socket.listen(5)

        # add to the full 'select()' collection
        if serial_socket in self._conn_list:
            self._conn_list.remove(serial_socket)
        self._conn_list.append(serial_socket)

        # add to the client 'lookup' collection
        if serial_socket in self._client_list:
            del self._client_list[serial_socket]
        self._client_list = {serial_socket: None}

        # add to the serial-client specific collection
        if serial_socket in self.serial_listeners:
            self.serial_listeners.remove(serial_socket)
        self.serial_listeners.append(serial_socket)
        return

    def select_loop(self):
        """
        Handle 1 select cycle
        """

        self.can_read, self.can_write, self.can_exec = select.select(self._conn_list, [], [], self.select_timeout)
        now = time.time()

        # handle any reading
        for sock in self.can_read:
            logger.debug("CanRead({}".format(sock))

            if sock == self.tls_control_listener:
                # then is a connection request on CONTROL socket
                self.control_accept()

            elif sock in self.serial_listeners:
                # then is a connection request on SERIAL socket
                self.serial_start()

            else:  # is one of the clients sending to serial
                client = self._client_list[sock]
                assert isinstance(client, Client)

                if not client.receive(now):
                    self.remove_client(sock)
                    client.close()
                    del client

        # handle any writing?
        for sock in self.can_write:
            logger.debug("CanWrit({}".format(sock))

        # handle any execution?
        for sock in self.can_exec:
            logger.debug("CanExec({}".format(sock))
            assert sock != self.tls_control_listener
            # client = self._client_list[sock]
            # self.remove_client(sock)
            # client.close()
            # del client

        # allow the client to idle-out things
        for sock in self._conn_list:
            if sock != self.tls_control_listener:
                client = self._client_list[sock]
                if client is not None:
                    assert isinstance(client, Client)
                    result = client.tick(now)
                    if result:
                        # then the client should process something
                        client.process(now)

        # allow the raw serial resource to do things
        for obj in self.serial_list:
            assert isinstance(obj, SerialObject)
            result = obj.tick(now)
            # if result:
            #     # then the client should process something
            #     client.process(now)

        logger.debug("Tick %s" % time.strftime("%H:%M:%S", time.localtime()))

        return True

    def add_control_client(self, connection, address):
        """
        We have detected an incoming connection request on the control socket.

        :param connection: socket.socket resource
        :param address: an IP tuple of the source IP/port, such as ("127.0.0.1", 54725)
        :return:
        """

        if connection in self._conn_list:
            # make sure we don't duplicate, put the new connection at END of the list
            self._conn_list.remove(connection)

        self._conn_list.append(connection)

        # create our client, and link it in here
        client = ControlClient()
        client.set_parent(self)
        client.set_logger(logger)
        client.connection = connection
        client.address = address
        client.recv_size = SOCKET_BUFFER_SIZE
        client.send_size = SOCKET_BUFFER_SIZE

        # add to the key-by-socket dictionary
        self._client_list = {connection: client}

        logger.debug("Connection from control peer:{0}:{1}".format(address[0], address[1]))

        return

    def add_serial_client(self, connection, address):
        """
        We have detected an incoming connection request on one of the serial sockets.

        :param connection: socket.socket resource
        :param address: an IP tuple of the source IP/port, such as ("127.0.0.1", 54725)
        :return:
        """

        if connection in self._conn_list:
            # make sure we don't duplicate, put the new connection at END of the list
            self._conn_list.remove(connection)

        self._conn_list.append(connection)

        # we don't care about this: self.serial_listeners = []

        # create our client, and link it in here
        client = SerialClient(0)
        client.set_parent(self)
        client.set_logger(logger)
        client.connection = connection
        client.address = address
        client.recv_size = SOCKET_BUFFER_SIZE
        client.send_size = SOCKET_BUFFER_SIZE

        # add to the key-by-socket dictionary
        self._client_list = {connection: client}

        logger.debug("Connection from serial peer:{0}:{1}".format(address[0], address[1]))

        return

    def remove_client(self, connection):

        # this should not happen
        assert self.tls_control_listener != connection

        # remove from both of our lists
        logger.debug("Remove a peer")
        self._conn_list.remove(connection)
        self._client_list.pop(connection)

        # do some simple clean-up
        gc.collect()

        return

    def get_report(self):
        """
        :return:
        """
        result = []

        for x in self._conn_list:
            if x != self.tls_control_listener:
                client = self._client_list[x]
                result.append(client.get_report())

        for x in self.serial_list:
            result.append(x.get_report())

        return result


def run_socket_listener():
    """
    This does not return.

    :return:
    """
    listener = ControlSocket()
    listener.control_start()

    for x in range(0, listener.max_port):
        obj = SerialObject(x)
        obj.set_parent(listener)
        listener.serial_list.append(obj)
        logger.info("Initialize serial_resource {0}".format(obj.get_name()))

    while listener.select_loop():
        pass

    return


if __name__ == '__main__':
    global logger

    logger = logging.getLogger('test')
    logging.basicConfig()

    # _logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    test_settings = SerialSettings()
    # test_settings._logger = _logger

    # the major core settings
    test_settings.put_value("control_mode", None, "tcp")
    test_settings.put_value("control_port", None, 2001)
    test_settings.put_value("max_ports", None, 1)

    test_settings.put_value("ip_mode", 0, "tcp")
    test_settings.put_value("ip_port", 0, 2101)
    test_settings.put_value("ser_port", 0, "COM5")
    test_settings.put_value("net_encode", 0, "binary")
    test_settings.put_value("eoln", 0, "raw")

    test_settings.put_value("product", 0, "DTE")
    test_settings.put_value("baud", 0, 9600)
    test_settings.put_value("parity", 0, 'N')
    test_settings.put_value("databits", 0, 8)
    test_settings.put_value("stopbits", 0, 1)
    test_settings.put_value("flow_control", 0, 'None')
    test_settings.put_value("rts_output", 0, 'on')
    test_settings.put_value("dtr_output", 0, 'on')

    run_socket_listener()
