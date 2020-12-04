
from link.link import Link
from physical.tcp_client import Tcp_client

def service(mylabel,Tx_queue):
    # send_number = 0
    while True:
        # get data from other thread
        to_link_layer = Tx_queue.get()
        # link layer
        # find to_IP foward to client
        # get encrypt message to client
        link = Link(to_link_layer)
        to_mac, to_physical_layer = link.link()
        # to_message = to_mac,to_label,str(mylabel),to_message
        # physical: client
        client = Tcp_client(to_mac, to_physical_layer)
        client.start_client()

        #print("finished", send_number)
        #send_number = send_number+1 

