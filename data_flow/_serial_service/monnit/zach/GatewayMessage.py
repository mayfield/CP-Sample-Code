from monnit.zach.ByteOperations import ByteOperations

class GatewayMessage:
    # 64000000 00000000 02  00  0000  0000    0100          BD61330B C50E0255361B0100D4D49F020011F70066
    # APNID    Security Ver Seq Power MsgType Count Payload Time     MSG
    APNID = [0x85, 0x03, 0x00, 0x00]
    Security = [0x00, 0x00, 0x00, 0x00]
    Version = [0x02]
    Sequence = [0x00]
    Power = [0x00, 0x00]
    MsgType = [0x00, 0x00]

    def __init__(self, messages):
        self.message = GatewayMessage.APNID \
                + GatewayMessage.Security + \
                GatewayMessage.Version + \
                GatewayMessage.Sequence + \
                GatewayMessage.Power + \
                GatewayMessage.MsgType
        count = len(messages)
        countbytes = [count & 0x00FF, count & 0xFF00]
        self.message += countbytes
        self.payload = []
        for k, v in messages.items():
            print("Time: %s, Message: %s" % (k, [hex(b) for b in v]))
            self.payload += ByteOperations.IntToLittleEndianBytes(int(k.total_seconds()), 4)
            self.payload += [iv for iv in v]
        print(self.payload)
        self.message += self.payload
        print("Gateway Message: \n\t%s" % self.message)
        self.Sequence[0] = self.Sequence[0]+1

    def getMessage(self):
        """

        :return:
        :rtype: bytes
        """
        self.message = bytes(self.message)
        return self.message
