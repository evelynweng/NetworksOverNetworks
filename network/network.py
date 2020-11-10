
from link.link import Link
from physical.tcp_client import Tcp_client


from security_evelyn.key_exchange import DiffieHellman, KeyExchange
from security_evelyn.symmetric_encryption import SymmetricEncryption


class Network():
    def __init__(self, to_network_layer,shared_keys):
        network_data = to_network_layer.split(",")
        # to_label,mylabel,idtfier,seqnum,payload
        self.to_label = network_data[0]
        self.from_label = network_data[1]
        self.identifier  = network_data[2]
        self.seqnum   = network_data[3]
        self.payload  = ','.join(network_data[4 : ])

    def network(self, to_network_layer,shared_keys):
        to_link_layer = self.secure_messaging(shared_keys)
        return to_link_layer
    
    def secure_messaging(self,shared_keys):
        print("secure messaging handshake")
        ke1 = KeyExchange()
        key_exchange_payload = ke1.key_exchange_payload(self.to_label,shared_keys,True)
        self.key_exchange_send(key_exchange_payload)
        print("start to wait for return public_key")
        while not (shared_keys[str(self.to_label)]): # busy wait for key to come in
            continue
        print("get the pubkey from target")
        public_key_from_target = shared_keys[str(self.to_label)]
        temp=ke1.ack_key_exchange_payload(self.to_label,shared_keys, public_key_from_target)
        shared_key = shared_keys[self.to_label] 
        cipher = SymmetricEncryption(shared_key)
        print("secure_messaging shared_key:", shared_key)
        print("self.payload.encode():", self.payload.encode())
        ciphertext = cipher.encrypt(self.payload.encode())
        print("encrypt message:", ciphertext)
        shared_keys.pop(self.to_label) #delete key
        print("delete used key:",self.to_label)
        return self.to_label+","+self.from_label+","+"message"+","+self.seqnum+","+ciphertext.hex()

    def key_exchange_send(self, key_exchange_payload):
        print("key exchange send")
        to_link_layer = self.to_label+","+self.from_label+","+"key_request"+","+self.seqnum+","+key_exchange_payload.hex()
        link = Link()
        to_mac = link.find_next_mac(to_link_layer)
        to_message = link.add_header_to_message(to_link_layer)
        
        # to_message = to_mac,to_label,str(mylabel),to_message
        # physical: client
        client = Tcp_client(to_mac, to_message)
        client.start_client()


    def get_pubic_key(self,shared_keys):
        print("get public key for source")
        ke2 = KeyExchange()
        ke2_public = ke2.ack_key_exchange_payload(self.from_label, shared_keys, bytes.fromhex(self.payload))
        print("shared key create:", shared_keys[self.from_label])
        print("return public key:", ke2_public)
        return ke2_public
    
    def forward_message (self, mylabel, to_network_layer,shared_keys):
        print(__name__, mylabel, to_network_layer)
        if self.match_label(mylabel, to_network_layer):
            new_to_label = self.from_label
            message = self.payload
            print ("this server received:" + message +" from: "+ new_to_label)
            
            if self.get_identifier()=="key_request" :
                print("key request")
                public_key = self.get_pubic_key(shared_keys)
                to_link_layer = new_to_label+","+mylabel+","+"ack_key_request"+","+self.seqnum+","+ public_key.hex()
                return to_link_layer

            if self.get_identifier()=="ack_key_request" :
                print("ack_key request")
                public_key = bytes.fromhex(message)
                shared_keys[new_to_label] = public_key
                print("get ack public_key:", shared_keys[new_to_label])
                return None

            if self.get_identifier() == "message":
                message = self.message_decrypt(message,shared_keys)
                print ("decrypt message:" + message +" from: "+ new_to_label)
                return new_to_label+","+mylabel+","+"ACK"+","+self.seqnum+","+"ACK"

            if self.get_identifier() == "ACK" :
                # ackflag = 1
                return None
            else:
                return new_to_label+","+mylabel+","+"ACK"+","+self.seqnum+","+"ACK"

        else: #not match keep sending message
            return to_network_layer
    
    # support functions (method that can be change): 

    def message_decrypt(self,message,shared_keys):
        print("message decrypt")
        shared_key = shared_keys.get(str(self.from_label), None)
        shared_keys.pop(self.from_label) 

        print("message_decrypt", shared_key)
        # delete key after exchange
        cipher = SymmetricEncryption(shared_key)
        print(bytes.fromhex(message))
        plaintext = cipher.decrypt(bytes.fromhex(message))
        print(plaintext)
        return plaintext.decode()

    def match_label(self, mylabel, to_network_layer):
        
        return self.to_label == mylabel
    
    def get_from_label(self, to_network_layer):
        return self.from_label

    def get_to_label(self, to_network_layer):
        return self.to_label
        
    def get_payload(self, to_network_layer):

        return self.payload

    def get_identifier (self):
        return self.identifier