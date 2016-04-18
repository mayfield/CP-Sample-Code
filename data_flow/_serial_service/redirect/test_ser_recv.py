__author__ = 'Lynn'

import serial
import codecs


if __name__ == '__main__':

    ser = serial.Serial("COM5", timeout=1.0)

    while True:
        response = ser.read(size=1024)
        if response is None or len(response) == 0:
            print("See:None")
        else:
            response = codecs.escape_encode(response)[0]
            print("See:{0}".format(response))
