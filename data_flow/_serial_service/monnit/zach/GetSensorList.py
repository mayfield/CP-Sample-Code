#!/usr/bin/python

import serial
import time
import datetime
import sys
from monnit.zach.CommandGenerator import CommandGenerator as cmdGen
from monnit.zach.GatewayMessage import GatewayMessage as GW
from monnit.zach.MonnitTcp import TcpClient as TcpClient
from monnit.zach.SensorListRequest import SensorListRequest
from monnit.zach.ByteOperations import ByteOperations

messageList = {}


def processResponse(response):	
    pass
    #print ", ".join([hex(ord(char)) for char in response])


def getTime():
    MonnitEpoch = time.mktime(datetime.datetime(2010, 1, 1, 0, 0).timetuple())
    now = int(time.time()-MonnitEpoch)
    timearray = [now & 0xFF000000, now & 0x00FF0000, now & 0x0000FF00, now & 0x000000FF]
    return timearray


def sendMessage(message: bytes):
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
        port='/dev/ttyUSB0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        timeout=.1
    )

APNID = ByteOperations.IntToLittleEndianBytes(901, 4)
request = SensorListRequest(APNID)
sensorList = request.GetSensorList()
print(sensorList)
for sensor in sensorList:
    addSensorRequest = cmdGen.addNetworkDeviceRequest(ByteOperations.IntToLittleEndianBytes(sensor, 4), 0x00)
    print([hex(ord(i)) for i in sendMessage(addSensorRequest)])

# sys.exit()

i = 0
while True:
    queuedMessageRequest = cmdGen.getQueuedMessageRequest([0x85,0x03,0x00,0x00], i, 0x00)
    print([hex(num) for num in queuedMessageRequest])
    data = sendMessage(queuedMessageRequest)
    print("Response from gateway: \n\t%s" % ", ".join([hex(ord(d)) for d in data]))
    try:	
        dataResponseCmd = data[3]
        dataResponseCode = data[8]
        if dataResponseCmd == 0x24 and dataResponseCode == 0xc:
            break
        else:
            messageList["".join([str(t) for t in getTime()])] = data
    except:
        pass  # probably out of range on data array
    i += 1
    i %= 256

messagePacket = GW(messageList)
response = TcpClient.SendData(messagePacket.getMessage())
readableresponse = [hex(item) for item in response]

print("Response from Server: \n\t%s" % readableresponse)

print('serial closed')
ser.close()
