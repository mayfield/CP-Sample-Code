class ByteOperations: 
    @staticmethod
    def LittleEndianBytesToInt(b):
        assert type(b) is list
        nb = b
        i = 0
        for byt in b:
            nb[i] = byt << (8 * i)
            i += 1
        return sum(nb)

    @staticmethod
    def IntToLittleEndianBytes(num, size):
        assert type(num) is int
        nnum = num
        b = [0 for i in range(size)]
        for i in range(len(b)):
            b[i] = (nnum >> (8 * i)) & 0xFF
        return b
