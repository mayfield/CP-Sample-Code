import socket

from monnit.format_bytes import format_bytes


class TcpClient:
    TCP_HOSTNAME="t1.sensorsgateway.com"
    TCP_PORT=3000

    BUFFER_SIZE=1024

    @staticmethod
    def SendData(data: bytes):

        text = format_bytes("TCP", data)
        print(text)
        dump_file = open("tcp_dump.txt", "a")
        dump_file.write("===")
        dump_file.write(text)
        dump_file.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TcpClient.TCP_HOSTNAME, TcpClient.TCP_PORT))
        s.send(data)
        response = s.recv(TcpClient.BUFFER_SIZE)
        s.close()
        return response
