import socket
import sys
sys.path.append("..")

from data_representation.deserialize import Deserialization
from data_representation.serialize import Serialization



serializer = Serialization()
deserializer = Deserialization()


UDP_SERVER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# get local machine name
LOCAL_IP = socket.gethostname()
LOCAL_PORT = 9999
BUFFER_SIZE = 1024
REPLY = str.encode("Server %s Message recived" % LOCAL_IP)

# bind to the port
UDP_SERVER.bind((LOCAL_IP, LOCAL_PORT))


print("UDP server runing on port: ", LOCAL_PORT)
print("Logs: ")

while True:
    # establish a connection, blocking here wait packet to come
    msg, client_info = UDP_SERVER.recvfrom(BUFFER_SIZE)
    msg_str_encrypted = msg.decode()
    msg_str = deserializer.deserialize(msg_str_encrypted)
    print("message %s from client %s" % (msg_str, client_info[0]))
    UDP_SERVER.sendto(REPLY, client_info)
