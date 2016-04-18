__author__ = 'Lynn'

import socket
import serial
import time
import codecs


if __name__ == '__main__':

    net = socket.socket()
    host = socket.gethostname()
    # host = "192.168.1.1"
    host = "192.168.0.208"
    # host = socket.gethostname()
    port = 7218
    net.connect((host, port))
    net.settimeout(2.0)

    while True:
        try:
            response = net.recv(1024)
            response = codecs.escape_encode(response)[0]
            print("See:{0}".format(response))

        except socket.timeout:
            print("See:None")

    net.close()
