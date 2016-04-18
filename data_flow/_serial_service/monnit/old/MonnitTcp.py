import socket


class TcpClient:
    TCP_HOSTNAME = "t1.sensorsgateway.com"
    TCP_PORT = 3000

    BUFFER_SIZE = 1024

    @staticmethod
    def send_data(data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TcpClient.TCP_HOSTNAME, TcpClient.TCP_PORT))
        s.send(data)
        response = s.recv(TcpClient.BUFFER_SIZE)
        s.close()
        return response
