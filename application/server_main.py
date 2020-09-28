from network.network import Network
from link.link import Link
from physical.tcp_client import Tcp_client
from physical.tcp_server import Tcp_server
from application import client_main 

def service(mylabel):
	#physical layer
	print("thread server")
	tcp_server = Tcp_server()
	while 1:
		# to_mac,to_label,str(mylabel),to_message
		receive_message = tcp_server.recv() # Blocking mode
		if not receive_message:
			# Return 0 if peer requets to terminate the connection
			continue

		# link layer
		# take off to_mac
		link = Link()
		to_network_layer = link.de_header_receive_message(receive_message)
		
		print(__name__, to_network_layer)
		
		# network layer
		network = Network()
		to_link_layer = network.forward_message(mylabel, to_network_layer)
		
		
		if to_link_layer == None:
			
			continue
			# got an "ACK" go back to the server_service loop
			# reopen server
		else:
			# __init client service to forward or sent ack message
			# cannot test on self->self message, will error.
			client_main.system_forward_message(mylabel, to_link_layer)
	

	
if __name__ == "__main__":
	service(123)