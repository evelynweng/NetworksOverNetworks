from application.service_send_message import Service_send_message
from network.network import Network 
from transport.transport import Transport
from link.link import Link
from physical.tcp_client import Tcp_client
from timeit import default_timer as timer

def service(mylabel,shared_keys):
	#application layer
	while 1:
		
		print("You can currently send messages, ping and traceroute on this virtual network")
		print("please select service: 0 = message, 1 = ping, 2 = tranceroute")
		user_input = input('CMPE206>')
		command = user_input.split(' ')
	
		if user_input == '0':
			service_send_message = Service_send_message()
			to_transport_layer = service_send_message.message_service(mylabel)

		elif user_input == '1':
			print('ping')
			# service_ping = Service_ping()
			# to_network_layer = service_ping.ping_service(mylabel,command[1])
		elif user_input == '2':
			print(command[1])
		else:
			continue
		#transport layer
		
		transport = Transport(to_transport_layer, shared_keys)
		to_network_layer = transport.transport(shared_keys) 

		#network layer
		network=Network(to_network_layer, shared_keys)
		to_link_layer = network.network(to_network_layer)

		# link layer
		# find to_IP foward to client

		link = Link(to_link_layer)
		to_mac, to_physical_layer = link.link()
		

		# to_message = to_mac,to_label,str(mylabel),to_message
		# physical: client
		client = Tcp_client(to_mac, to_physical_layer)
		client.start_client()

		continue


def system_forward_message(to_link_layer):
	# link layer
	# find to_IP foward to client

	link = Link(to_link_layer)
	to_mac, to_physical_layer = link.link()
	
	# physical: client
	client = Tcp_client(to_mac, to_physical_layer)
	client.start_client()
	



if __name__ == "__main__":
	service(123)