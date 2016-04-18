import array
import logging

from common.format_bytes import format_bytes


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
        """

        :param messages:
        :type messages: dict
        :return:
        """
        self.message = GatewayMessage.APNID + \
            GatewayMessage.Security + \
            GatewayMessage.Version + \
            GatewayMessage.Sequence + \
            GatewayMessage.Power + \
            GatewayMessage.MsgType

        count = len(messages)
        count_bytes = [count & 0x00FF, count & 0xFF00]
        logging.debug("Count: %s", [hex(b) for b in count_bytes])
        self.message += count_bytes
        self.payload = []
        for k, v in messages.items():
            logging.debug("Time: %s, Message: %s", k, [hex(b) for b in v])
            self.payload += k
            self.payload += v
        self.payload = [ord(p) for p in self.payload]
        self.message += self.payload
        logging.debug(format_bytes("Gateway Message", bytes(self.message)))
        self.Sequence[0] += 1

    def get_message(self):
        # self.message = bytearray.fromhex("85 03 00 00 00 00 00 00 02 00 00 00 00 00 00 00")
        self.message = array.array('B', self.message)
        return self.message
