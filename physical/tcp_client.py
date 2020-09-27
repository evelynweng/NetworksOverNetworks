import socket


class Tcp_client():
    def __init__(self, to_mac, to_message):
        self.tcpip = to_mac
        self.send_message = to_message
    
    def start_client(self):
        TCP_IP = self.tcpip
        TCP_PORT = 9999
        BUFFER_SIZE = 1024
        MESSAGE = self.send_message.encode()

        print(__name__, TCP_IP)
        #print(MESSAGE)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("socket")
        s.connect((TCP_IP, TCP_PORT))
        #print("connected")
        #print(__name__, "Sending")

        s.send(MESSAGE)

        print(__name__, "Sent, wait for recv")

        data = s.recv(BUFFER_SIZE)

        print(__name__, "Recved")

        s.close()

        print ("received data:", data.decode())