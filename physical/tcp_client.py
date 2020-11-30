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

        #print(__name__, TCP_IP)
        #print(MESSAGE)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)   # set time  out to 5 sececod

        try:
            s.connect((TCP_IP, TCP_PORT))
        except socket.error as exc:
            print ("Caught exception socket.error : %s" % exc)
            s.close()
            return 0

        s.send(MESSAGE)

        #print(__name__, "Sent, wait for recv")

        data = s.recv(BUFFER_SIZE)

        print(__name__, "Recved")

        s.close()

        #print ("client socket close")