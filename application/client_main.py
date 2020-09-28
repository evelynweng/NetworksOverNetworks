from application.service_send_message import Service_send_message
from network.network import Network 
from link.link import Link
from physical.tcp_client import Tcp_client
from timeit import default_timer as timer

def service(mylabel):
	#application layer
	while 1:
		service_send_message = Service_send_message()
		to_network_layer = service_send_message.message_service(mylabel)
		
		#transport layer
			# do nothing

		#network layer
			# 9/15 do nothing just forward message 
		network=Network()
		to_link_layer = network.network(to_network_layer)

		# link layer
		# find to_IP foward to client
		# get encrypt message to client
		link = Link()
		to_mac = link.find_next_mac(to_link_layer)
		to_message = link.add_header_to_message(to_link_layer)

		# to_message = to_mac,to_label,str(mylabel),to_message
		# physical: client
		client = Tcp_client(to_mac, to_message)
		client.start_client()

		break


def system_forward_message(mylabel, to_link_layer):
	# link layer
	# find to_IP foward to client
	# get encrypt message to client
	link = Link()
	to_mac = link.find_next_mac(to_link_layer)
	to_message = link.add_header_to_message(to_link_layer)

	# to_message = to_mac,to_label,str(mylabel),to_message
	# physical: client
	client = Tcp_client(to_mac, to_message)
	client.start_client()
	



if __name__ == "__main__":
	service(123)