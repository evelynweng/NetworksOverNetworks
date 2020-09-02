import socket

UDP_SERVER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# get local machine name
LOCAL_IP = socket.gethostname()                           
LOCAL_PORT = 9999
BUFFER_SIZE = 1024
REPLY = str.encode("Server %s Message recived" %LOCAL_IP)

# bind to the port
UDP_SERVER.bind((LOCAL_IP, LOCAL_PORT))                                  

print("UDP server runing on port: ",LOCAL_PORT) 
print("Logs: ")

while True:
    #establish a connection
    msg,client_info = UDP_SERVER.recvfrom(BUFFER_SIZE)
    print("message %s from client %s" % (msg.decode(), client_info[0]))
    UDP_SERVER.sendto(REPLY, client_info)
