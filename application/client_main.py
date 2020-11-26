from transport.transport import Transport
from network.network import Network 
from link.link import Link
from physical.tcp_client import Tcp_client

from application.service_send_message import Service_send_message
from application.ping_service import Ping_service
from application.traceroute_service import Traceroute_service

def service(mylabel,shared_keys,Tx_queue):
	#application layer
	while 1:
		
		print("You can currently send messages, ping and traceroute on this virtual network")
		print("please select service: message, ping: ping .destination, tranceroute: traceroute .destination")
		user_input = input('CMPE206>')
		command = user_input.split(' ')
	
		if user_input == 'message':
			service_send_message = Service_send_message()
			to_transport_layer = service_send_message.message_service(mylabel)
			transport = Transport(to_transport_layer)
			to_network_layer = transport.transport(shared_keys,Tx_queue) 

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
			# network layer
			network = Network(to_network_layer, shared_keys)
			to_link_layer = network.network(to_network_layer)
			Tx_queue.put(to_link_layer)
			
		elif isinstance(to_network_layer,list):
			for packet in to_network_layer:
				network = Network(packet, shared_keys)
				to_link_layer = network.network(packet)
				Tx_queue.put(to_link_layer)

		else:
			print("to_network_layer format invalid")

		continue

def system_forward_message(to_link_layer,Tx_queue):
	Tx_queue.put(to_link_layer)
	
if __name__ == "__main__":
	service(123)