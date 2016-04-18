__author__ = 'Lynn'

import socket
import time
import codecs


def send_one(net_sock, ser_han, request):

    print("See:{0}".format(codecs.escape_encode(request)[0]))
    net_sock.send(request)
    time.sleep(1.5)

    return


if __name__ == '__main__':

    net = socket.socket()
    # host = "192.168.1.1"
    host = "192.168.0.208"
    # host = socket.gethostname()
    port = 7218
    net.connect((host, port))

    data = [
        b"Hello",
        b"Hello\r\n",
        b"Hello\n",
        b"Hello\r",
        b"Hello\xFF\xFF",
        b"\x01\x03\x00\x00\x00\x05\xAB\x14",
        b"Hello\r\nTop",
        b"Hello\nTop",
        b"Hello\rTop",
        b"Hello\xFF\xFFTop"
        ]

    for datum in data:
        send_one(net, None, datum)

    net.close()
