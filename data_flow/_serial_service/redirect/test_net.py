__author__ = 'Lynn'

import socket
import serial
import time
import codecs


def send_one(net_sock, ser_han, request):

    print("See:{0}".format(codecs.escape_encode(request)[0]))
    net_sock.send(request)
    time.sleep(1.0)

    return


if __name__ == '__main__':

    net = socket.socket()
    host = socket.gethostname()
    port = 10000
    net.connect((host, port))

    ser = serial.Serial("COM6", timeout=1.0)

    data = [
        b"Hello\r\n",
        b"Hello\n",
        b"Hello\r",
        b"Hello\xFF\xFF",
        b"\x01\x03\x00\x00\x00\x05\xAB\x14",
        b"Hello\r\nTop",
        b"Hello\nTop",
        b"Hello\rTop",
        b"Hello\xFF\xFFTop",
        ]

    for datum in data:
        send_one(net, ser, datum)

    net.close()
