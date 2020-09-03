import socket

"""
this is a example for socket programing on udp server
"""
# create a socket object
UDP_CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# get local machine name
server_info = ("35.161.72.250", 9999)
MESSAGE =["hello", "mess1", "mmess2",
        "mess3","m2asd","thisme2","gasdw2","geads2","mg3"]
BUFFER_SIZE = 1024

for m in MESSAGE:
    UDP_CLIENT.sendto(m.encode(), server_info)
    msg = UDP_CLIENT.recvfrom(BUFFER_SIZE)
    print(msg[0].decode())

