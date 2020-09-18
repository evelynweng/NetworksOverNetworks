import socket
import sys
sys.path.append("..")

from data_representation.deserialize import Deserialization
from data_representation.serialize import Serialization

serializer = Serialization()
deserializer = Deserialization()


"""
this is a example for socket programing on udp server
"""
# create a socket object
UDP_CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server_info[0] should be the server's ip address, server_info[1] should be the port that is hosting on the server
# 35.161.72.250 us my ec2 public ipv4 address
# 9999 is my ec2 host port
ip_address = input("Please input the IP address to send: ")
port = input("Please input the port of the IP address to send: ")
server_info = (ip_address, int(port))
#server_info = ("34.123.189.50", 9999)
input_str = input("Please input text you would like to serialize: ")
BUFFER_SIZE = 1024
msg_encrpted = serializer.serialize(input_str)
UDP_CLIENT.sendto(msg_encrpted.encode(), server_info)
msg = UDP_CLIENT.recvfrom(BUFFER_SIZE)
print(msg[0].decode())
