#!/usr/bin/env python

import socket
class Tcp_server():
    def __init__(self):
        self.TCP_IP = socket.gethostname() #default local host name
        self.TCP_PORT = 9999
        self.BUFFER_SIZE = 1024  # Normally 1024

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)
        print ("start listen")

    def recv(self):
        print("server waits for connection ..")
        self.conn, self.addr = self.s.accept()
        print ('Connection address:', self.addr)
        data = self.conn.recv(self.BUFFER_SIZE)
        if data:
            data = data.decode()
            print ("received data:", data)
            self.conn.send("router ack".encode())  # echo
        self.conn.close()
        return data