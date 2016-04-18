"""
The raw protocol processors

The protocol seems to be:
- [00] = 0xC5 is first byte
- [01] = a command byte such as 0x20, etc
- [02] = length in bytes of payload NOT including the cmd+len
"""


class CommandGenerator:
    firstByte = 0xC5

    class FlagByte:
        NoFlag = 0x00
        Urgent = 0x02
        WaitingForQueued = 0x04

    class CommandByte:
        """
        Enum for command codes and size of their accompanying bytes. For example, the Form Network request is 0x20,
        and has 5 extra bytes of data, so the length is 5. If multiple sizes are possible, the largest one is listed.
        """
        FormNetworkRequest = (0x20, 5)
        UpdateNetworkStateRequest = (0x21, 5)
        RegisterWirelessDeviceRequest = (0x22, 4)
        NetworkStatusReport = (0x23, 10)
        QueuedMessageRequest = (0x24, 5)
        WirelessDeviceStatusReport = (0x25, 7)
        RegisteredDeviceListRequest = (0x26, 1)
        RegisteredSensorListResponse = (0x27, 17)
        ReadDataSectorRequest = (0x70, 5)
        ReadDataSectorResponse = (0x71, 38)
        WriteDataSectorRequest = (0x72, 37)
        WriteDataSectorResponse = (0x73, 6)
        ApplicationCommandRequest = (0x74, 43)
        ApplicationCommandResponse = (0x75, 43)
        DataMessageReport = (0x55, 42)
        DataLoggedSensorDataMessage = (0x56, 46)
        ParentMessage = (0x52, 12)

        # From here forward, the commands are for MODBUS Gateway Only
        BootloaderCommandRequest = (0xD4, 39)
        BootloaderCommandResponse = (0xD5, 8)

    @staticmethod
    def get_crc(message):
        """
        Given the message as a list of ints, return CRC as an int

        :param message:
        :type message: list
        :return:
        :rtype: int
        """
        crc = 0
        for i in range(2, message[1] + 2):
            crc = CommandGenerator.add_step2_crc(crc, message[i])
        return crc

    @staticmethod
    def add_step2_crc(crc, next_byte):
        """

        :param crc: the initial CRC, which starts as 0
        :type crc: int
        :param next_byte:
        :type next_byte: int
        :return: the final CRC as 8-bit byte
        :rtype: int
        """
        crc = (crc ^ next_byte) & 0xFF  # xor with next_byte
        for j in range(0, 8):
            if (crc & 0x80) == 0x80:
                crc = ((crc << 1) & 0xFF) ^ 0x97
            else:
                crc <<= 1
            crc &= 0xFF
        return crc

    @staticmethod
    def get_form_network_request(channel_mask, network_id, flag):
        """

        :param channel_mask:
        :type channel_mask: list
        :param network_id:
        :type network_id: int
        :param flag:
        :type flag: int
        :return:
        """
        assert type(channel_mask) is list
        assert type(network_id) is int
        assert type(flag) is int

        command = list()
        command.append(CommandGenerator.firstByte)
        command_pair = CommandGenerator.CommandByte.FormNetworkRequest
        command.append(command_pair[1] + 2)     # add the length + 2
        command.append(flag)                    # add the QOS byte (urgent, etc)
        command.append(command_pair[0])         # add the command byte
        command += channel_mask                 # add the channel mask
        command.append(network_id)
        command.append(CommandGenerator.get_crc(command))
        return command

    @staticmethod
    def get_queued_message_request(device_id, message_status, flag):
        """

        :param device_id:
        :type device_id: list
        :param message_status:
        :type message_status: int
        :param flag:
        :type flag: int
        :return:
        """
        assert type(device_id) is list
        assert type(message_status) is int

        command = [CommandGenerator.firstByte]
        command_pair = CommandGenerator.CommandByte.QueuedMessageRequest
        command.append(command_pair[1]+2)
        command.append(flag)
        command.append(command_pair[0])
        command += device_id
        command.append(message_status)
        command.append(CommandGenerator.get_crc(command))
        return command
