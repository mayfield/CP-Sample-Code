#!/usr/bin/python

import serial
import time
import datetime
import logging

from common.format_bytes import format_bytes
from monnit.CommandGenerator import CommandGenerator as cmdGen
from monnit.GatewayMessage import GatewayMessage as Gateway
from monnit.MonnitTcp import TcpClient as TcpClient

messageList = {}


def process_response(response):
    pass
    # print ", ".join([hex(ord(char)) for char in response])


def get_time():
    monnit_epoch = time.mktime(datetime.datetime(2010, 1, 1, 0, 0).timetuple())
    now = int(time.time() - monnit_epoch)
    time_array = [now & 0xFF000000, now & 0x00FF0000, now & 0x0000FF00, now & 0x000000FF]
    return time_array


def send_message(ser, message):
    """

    :param ser:
    :type ser: serial.Serial
    :param message:
    :type message: bytes
    :return:
    """
    if not isinstance(message, bytearray):
        message = bytearray(message)

    logging.debug(format_bytes("SND", message))
    ser.write(message)

    data = b""
    while True:
        previous = data
        data += ser.read()
        if previous == data:
            break

    logging.debug(format_bytes("RCV", data))

    process_response(data)

    return data


def main():

    # port='/dev/ttyUSB0',
    port_name = 'COM15',

    logging.info("Opening Gateway on port:{}".format(port_name))
    ser = serial.Serial(
            # port='/dev/ttyUSB0',
            port='COM15',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            timeout=.1
    )

    active_message = bytearray.fromhex("c5 07 00 21 01 39 b5 31 0b 1e")
    idle_message = bytearray.fromhex("c5 07 00 21 00 a8 b4 31 0b f8")

    send_message(ser, active_message)

    i = 0
    while True:
        queued_message_request = cmdGen.get_queued_message_request([0x85, 0x03, 0x00, 0x00], i, 0x00)
        # logging.info(format_bytes("DAT", queued_message_request))

        data = send_message(ser, queued_message_request)

        try:
            data_response_cmd = data[3]
            data_response_code = data[8]
            if data_response_cmd == 0x24 and data_response_code == 0xc:
                break
            else:
                messageList["".join([str(t) for t in get_time()])] = data
        except IndexError:
            pass  # probably out of range on data array
        i += 1
        i %= 256

    message_packet = Gateway(messageList)
    response = TcpClient.send_data(message_packet.get_message())
    # readable_response = [hex(item) for item in response]

    logging.debug(format_bytes("Response from Server", bytes(response)))

    logging.info('serial closed')
    ser.close()

    return

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    main()
