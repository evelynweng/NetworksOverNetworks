from transport.transport import Transport
from network.network import Network 
from link.link import Link
from physical.tcp_client import Tcp_client

from application.service_send_message import Service_send_message
from application.ping_service import Ping_service
from application.traceroute_service import Traceroute_service

def service(mylabel,shared_keys):
	#application layer
	while 1:
		
		print("You can currently send messages, ping and traceroute on this virtual network")
		print("please select service: message, ping: ping .destination, tranceroute: traceroute .destination")
		user_input = input('CMPE206>')
		command = user_input.split(' ')
	
		if user_input == 'message':
			service_send_message = Service_send_message()
			to_transport_layer = service_send_message.message_service(mylabel)
			transport = Transport(to_transport_layer, shared_keys)
			to_network_layer = transport.transport(shared_keys) 

		elif command[0] == 'ping':
			ping_send_service = Ping_service()
			to_network_layer = ping_send_service.ping_send_service(mylabel, command[1])
		elif command[0] == 'traceroute':
			traceroute_send_service = Traceroute_service()
			to_network_layer = traceroute_send_service.traceroute_send_service(mylabel, command[1])
		else:
			continue
		#transport layer

		if isinstance(to_network_layer,str):
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
			
		elif isinstance(to_network_layer,list):
			for packet in to_network_layer:
				# transport layer
					# do nothing
				# network layer
				# 9/15 do nothing just forward message
				network = Network(packet, shared_keys)
				to_link_layer = network.network(packet)
				# link layer
				# find to_IP foward to client
				# get encrypt message to client
				link = Link(to_link_layer)
				to_mac, to_physical_layer = link.link()
				# to_message = to_mac,to_label,str(mylabel),to_message
				# physical: client
				client = Tcp_client(to_mac, to_physical_layer)
				client.start_client()
		else:
			print("to_network_layer format invalid")

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