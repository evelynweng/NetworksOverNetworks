from network.network import Network
from link.link import Link
from physical.tcp_client import Tcp_client

from security.key_exchange import DiffieHellman, KeyExchange
from security.symmetric_encryption import SymmetricEncryption


class Transport():
    def __init__(self, to_transport_layer,shared_keys):
        network_data = to_transport_layer.split(",")
        # to_label,mylabel,idtfier,seqnum,payload
        self.to_label = network_data[0]
        self.from_label = network_data[1]
        self.identifier  = network_data[2]
        self.seqnum   = network_data[3]
        self.payload  = ','.join(network_data[4 : ])
        self.forward_message = to_transport_layer

    def transport(self, shared_keys):
        if (self.identifier == "message"):
            to_network_layer = self.secure_messaging(shared_keys)
        else:
            to_network_layer = self.forward_message
        return to_network_layer

    def secure_messaging(self,shared_keys):
        #print("secure messaging handshake")
        ke1 = KeyExchange()
        key_exchange_payload = ke1.key_exchange_payload(self.to_label,shared_keys,True)
        self.key_exchange_send(key_exchange_payload)

        while not (shared_keys[str(self.to_label)]): 
            continue
        #print("get the pubkey from target")

        public_key_from_target = shared_keys[str(self.to_label)]
        temp=ke1.ack_key_exchange_payload(self.to_label,shared_keys, public_key_from_target)
        shared_key = shared_keys[self.to_label] 
        cipher = SymmetricEncryption(shared_key)
        #print("secure_messaging shared_key:", shared_key)
        #print("self.payload.encode():", self.payload.encode())
        ciphertext = cipher.encrypt(self.payload.encode())
        print("encrypt message:", ciphertext)
        shared_keys.pop(self.to_label) #delete key
        #print("delete used key:",self.to_label)
        return (self.to_label+","+self.from_label+","
        +"message"+","+self.seqnum+","+ciphertext.hex())

    def key_exchange_send(self, key_exchange_payload):
        print("key exchange send")
        # generate network layer format to link layer
        to_link_layer = (self.to_label+","+self.from_label
            +","+"key_request"+","+self.seqnum+","+key_exchange_payload.hex())
       
        link = Link(to_link_layer)
        to_mac, to_physical_layer = link.link()

        # physical: client
        client = Tcp_client(to_mac, to_physical_layer)
        client.start_client()