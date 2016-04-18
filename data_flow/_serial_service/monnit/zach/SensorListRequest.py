import array
from monnit.zach.MonnitTcp import TcpClient
from monnit.zach.ByteOperations import *

class SensorListRequest:
    #64000000 00000000 02  00  0000  0000    0100          BD61330B C50E0255361B0100D4D49F020011F70066
    #APNID    Security Ver Seq Power MsgType Count Payload Time     MSG
    Security = [0x00, 0x00, 0x00, 0x00]
    Version = [0x02]
    Sequence = [0x00]
    Power = [0x00, 0x00]
    MsgType = [0x02, 0x00]
    def __init__(self, APNID):
        self.Sequence[0] = 0
        self.message = APNID \
                + SensorListRequest.Security + \
                SensorListRequest.Version + \
                SensorListRequest.Sequence + \
                SensorListRequest.Power + \
                SensorListRequest.MsgType
        count = [0, 0]
        self.message += count
        print("Sensor List Request: \n\t%s" % self.message)

    def getMessage(self):
        """

        :return:
        :rtype: bytes
        """
        #self.message = bytearray.fromhex("85 03 00 00 00 00 00 00 02 00 00 00 00 00 00 00")
        self.message = bytes(self.message)
        return self.message

    def GetSensorList(self):
        response = TcpClient.SendData(self.getMessage())
        intResponse = [ord(b) for b in response]
        sensorList = []
        i=18
        print("Sensor Count: %r" % intResponse[16])
        while (i+4) <= len(intResponse):
            sensorList.append(ByteOperations.LittleEndianBytesToInt(intResponse[i:i+4]))
            i+=4
        return sensorList
