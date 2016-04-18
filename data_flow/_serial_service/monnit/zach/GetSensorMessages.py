#!/usr/bin/python

import serial
import time
import datetime
import sys
from monnit.zach.CommandGenerator import CommandGenerator as cmdGen
from monnit.zach.GatewayMessage import GatewayMessage as GW
from monnit.zach.MonnitTcp import TcpClient as TcpClient
from monnit.zach.ByteOperations import ByteOperations

messageList = {}


def processResponse(response):	
    pass
    #print ", ".join([hex(ord(char)) for char in response])


def getTime():
    MonnitEpoch = datetime.datetime(2010, 1, 1, 0, 0)
    now = datetime.datetime.utcnow()
    time = now - MonnitEpoch
    return time


def sendMessage(message: bytes):
    """

    :param message:
    :return:
    :rtype: bytes
    """
    if type(message) is not bytearray:
        message = bytearray(message)
    ser.write(message)
    data = b""
    while True:
        previous = data
        data += ser.read()
        if previous == data:
            break
    processResponse(data)
    return data


ser = serial.Serial(
        # port='/dev/ttyUSB0',
        port=14,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        timeout=.1
    )

utcnow = int(getTime().total_seconds())
timearray = ByteOperations.IntToLittleEndianBytes(utcnow, 4)
activeMessage = cmdGen.getUpdateNetworkStateRequest(1, timearray, 0x00)

sendMessage(activeMessage)

while True:
    i = 0
    messageList = {}
    while True:
        queuedMessageRequest = cmdGen.getQueuedMessageRequest([0x85,0x03,0x00,0x00], i, 0x00)
        data = sendMessage(queuedMessageRequest)
        print("Response from gateway: \n\t%s" % ", ".join([hex(d) for d in data]))
        dataResponseCmd = data[3]
        dataResponseCode = data[8]
        if dataResponseCmd == 0x24 and dataResponseCode == 0xc:
            break
        else:
            t = getTime()
            print(t)
            messageList[t] = data
        i += 1
        i %= 256

    messagePacket = GW(messageList)
    response = TcpClient.SendData(messagePacket.getMessage())
    readableresponse = [hex(item) for item in response]
    print("Response from Server: \n\t%s" % readableresponse)

    time.sleep(10)


print('serial closed')
ser.close()
