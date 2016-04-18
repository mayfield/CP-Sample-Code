class CommandGenerator: 
    firstByte = 0xC5

    class FlagByte:
        NoFlag = 0x00
        Urgent = 0x02
        WaitingForQueued = 0x04

    class CommandByte:
        """
        Enum for command codes and size of their accompanying bytes. For example, the Form Network request is 0x20, and has 5 extra bytes of data, so the length is 5. If multiple sizes are possible, the largest one is listed.
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
        # From here forward, the commands are for MODBUS GW Only
        BootloaderCommandRequest = (0xD4, 39)
        BootloaderCommandResponse = (0xD5, 8)

    @staticmethod
    def getCRC(message: list):
        crc = 0
        for i in range(2, message[1] + 2):
            crc = CommandGenerator.AddStep2CRC(crc, message[i])
        return crc

    @staticmethod
    def AddStep2CRC(crc: int, nextByte: int):
        crc = (crc ^ nextByte) & 0xFF  # xor with nextByte
        for j in reversed(range(0, 8)):
            if (crc & 0x80) == 0x80:
                crc = (((crc << 1) & 0xFF) ^ 0x97) & 0xFF
            else:
                crc = (crc << 1)&0xFF
        return crc

    @staticmethod
    def getFormNetworkRequest(ChannelMask, NetworkID, Flag):
        assert type(ChannelMask) is list
        assert type(NetworkID) is int
        assert type(Flag) is int
        command = []
        command.append(CommandGenerator.firstByte)
        commandPair = CommandGenerator.CommandByte.FormNetworkRequest
        command.append(commandPair[1] + 2)
        command.append(Flag)
        command.append(commandPair[0])
        command += ChannelMask
        command.append(NetworkID)
        command.append(CommandGenerator.getCRC(command))
        return command

    @staticmethod
    def getQueuedMessageRequest(DeviceID, MessageStatus, Flag):
        assert type(DeviceID) is list
        assert type(MessageStatus) is int
        command = [CommandGenerator.firstByte]
        commandPair = CommandGenerator.CommandByte.QueuedMessageRequest
        command.append(commandPair[1] + 2)
        command.append(Flag)
        command.append(commandPair[0])
        command += DeviceID
        command.append(MessageStatus)
        command.append(CommandGenerator.getCRC(command))
        return command

    @staticmethod
    def addNetworkDeviceRequest(DeviceID, Flag):
        assert type(DeviceID) is list
        assert type(Flag) is int
        command = [CommandGenerator.firstByte]
        commandPair = CommandGenerator.CommandByte.RegisterWirelessDeviceRequest
        command.append(commandPair[1]+2)
        command.append(Flag)
        command.append(commandPair[0])
        command += DeviceID
        command.append(CommandGenerator.getCRC(command))
        return command

    @staticmethod
    def getUpdateNetworkStateRequest(state, timearray, Flag):
        assert type(state) is int
        assert type(timearray) is list
        assert type(Flag) is int
        command = [CommandGenerator.firstByte]
        commandPair = CommandGenerator.CommandByte.UpdateNetworkStateRequest
        command.append(commandPair[1]+2)
        command.append(Flag)
        command.append(commandPair[0])
        command.append(state)
        command += timearray
        command.append(CommandGenerator.getCRC(command))
        return command

