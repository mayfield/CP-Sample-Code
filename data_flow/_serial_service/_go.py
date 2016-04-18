__author__ = 'Lynn'

import logging
import sys
import socket
import time
import ssl
import json

from serial_settings import SerialSettings
import json_utility

PROMPT = "apa? "


class TestRig(object):

    HOST = "localhost"
    
    TLS_VERIFY = False

    def __init__(self):
        self.logger = None
        self._settings = SerialSettings()

        self._identifier = 1
        
        # self.tls_context = ssl.create_default_context()
        self.tls_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
        self.tls_context.verify_mode = self.TLS_VERIFY
        self.tls_context.check_hostname = self.TLS_VERIFY
        if self.TLS_VERIFY:
            self.tls_context.load_verify_locations('/etc')
        # else:
        self.tls_socket = None

        self.host = self.HOST

        return

    def set_logger(self, log_handler):
        self.logger = log_handler
        self.logger._settings = log_handler
        return

    def open(self, port=None):
        """
        Open the socket

        :param port:
        :return:
        """

        if port is None:
            port = self._settings.get_value("control_port", None)

        # start with the socket closed
        self.close()

        # then open
        self.tls_socket = self.tls_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.HOST)
        self.tls_socket.connect((self.HOST, port))

        if self.logger is not None:
            logger.info('Opened socket to ({0}:{1})'.format(self.host, port))

        return True

    def close(self):
        try:
            self.tls_socket.shutdown(socket.SHUT_RDWR)
            self.tls_socket.close()	
        except:
            pass
        self.tls_socket = None
        return

    def is_open(self):
        return self.tls_socket is not None
        
    def send(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
            
        return self.tls_socket.send(data.encode())

    def receive(self):
        data = self.tls_socket.recv(4092)
        if data:
            data = json.loads(data.decode())
            
        return data 
        
    def make_jsonrpc(self, method_name):
        """
        Send a NOP method

        :return:
        """
        self._identifier += 1
        return json_utility.make_jsonrpc_request(method_name, self._identifier)
        
    def echo(self):
        """
        Send an echo method

        :return:
        """

        if not self.is_open():
            logger.error('Socket is not Open')
            return False
            
        request = self.make_jsonrpc("echo")
        request["params"] = {"value": time.asctime()}
        
        if self.logger is not None:
            logger.debug('Send:{0}'.format(request))
            
        self.send(request)
        
        time.sleep(1.0)
        
        result = self.receive()
        
        if self.logger is not None:
            logger.debug('Recv:{0}'.format(result))

        return True

    def report(self):
        """
        Send a Report method
        
        {'method': 'report'}
        {'result': [{'status': 'active', 'name': '127.0.0.1.65290'},
                    {'status': 'closed', 'name': 'serial0'}, 
                    {'status': 'closed', 'name': 'serial1'}]
        }

        :return:
        """

        if not self.is_open():
            logger.error('Socket is not Open')
            return False
            
        request = self.make_jsonrpc("report")
        # request["params"] = None
        
        if self.logger is not None:
            logger.debug('Send:{0}'.format(request))
            
        self.send(request)
        
        time.sleep(1.0)
        
        result = self.receive()
        
        if self.logger is not None:
            logger.debug('Recv:{0}'.format(result))

        return True


if __name__ == '__main__':
    global logger

    logger = logging.getLogger('test')
    logging.basicConfig()

    # _logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    rig = TestRig()
    rig.set_logger(logger)

    while True:
        logger.debug('')
        if rig.is_open():
            logger.debug('Socket is Open')
        else:
            logger.debug('Socket is Closed')
        get_command = input(PROMPT).lower()

        if get_command == '':
            pass
            
        elif get_command == 'close':
            logger.debug('Command.close')
            rig.close()

        elif get_command == 'echo':
            logger.debug('Command.echo')
            rig.echo()

        elif get_command == 'open':
            logger.debug('Command.open')
            rig.open()

        elif get_command == 'quit':
            logger.debug('Command.quit')
            break

        elif get_command == 'report':
            logger.debug('Command.report')
            rig.report()

        else:
            logger.info('Help:')
            logger.info('  cert = dump the server cert')
            logger.info('  close = close the socket')
            logger.info('  open = open/reopen the socket')
            logger.info('  quit = exit')

    logger.info('Clean Exit')
