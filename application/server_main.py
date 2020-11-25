from network.network import Network
from link.link import Link
from physical.tcp_server import Tcp_server
from application import client_main 

def service(mylabel,shared_keys):
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
		to_network_layer = link.recv_message(receive_message)
		
		#not valid input or empty input
		if not to_network_layer:
			continue
		
		# network layer
		
		network = Network(to_network_layer,shared_keys)
		to_link_layer = network.recv_packet(mylabel,shared_keys)
		
		
		if to_link_layer == None:
			
			continue
			# got an "ACK" go back to the server_service loop
			# reopen server
		else:
			# __init client service to forward or sent ack message
			# cannot test on self->self message, will error.
			client_main.system_forward_message(to_link_layer)
	

	
if __name__ == "__main__":
	service(123)