import socket
import serial
import time
import binascii
import threading


# The target IP and TCP port of the router under test
ROUTER_IP = "192.168.0.208"
ROUTER_PORT = 7218


class NetClient(threading.Thread):

    def __init__(self, name):
        super().__init__()

        self.please_stop = threading.Event()
        self.please_stop.clear()
        self.net_han = None
        self.name = name
        return

    def run(self):

        self.net_han = socket.socket()
        self.net_han.connect((ROUTER_IP, ROUTER_PORT))
        self.net_han.settimeout(5.0)

        while not self.please_stop.is_set():
            # the run loop

            try:
                response = self.net_han.recv(1024)
                print("{0}:rsp:{1}".format(self.name, binascii.hexlify(response)))

            except socket.timeout:
                print("{0}:rsp:None".format(self.name))
                return 1

        self.net_han.close()
        return


if __name__ == '__main__':

    print("Start the Network Thread #1")
    net1_client = NetClient('net1')
    net1_client.start()

    time.sleep(300.0)
    net1_client.please_stop.set()
    net1_client.join()
