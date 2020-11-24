from security_evelyn.key_exchange import DiffieHellman, KeyExchange
from security_evelyn.symmetric_encryption import SymmetricEncryption


class Network():
    def __init__(self, to_network_layer,shared_keys):
        if to_network_layer :
            network_data = to_network_layer.split(",")
            # to_label,mylabel,idtfier,seqnum,payload
            self.to_label = network_data[0]
            self.from_label = network_data[1]
            self.identifier  = network_data[2]
            self.seqnum   = network_data[3]
            self.payload  = ','.join(network_data[4 : ])
            self.forward_message = to_network_layer #packet unchange

    def network(self, to_network_layer):
        to_link_layer = to_network_layer
        return to_link_layer
    
    def recv_packet (self, mylabel,shared_keys):
        # print(__name__, mylabel, to_network_layer)
        if self.match_label(mylabel):
            new_to_label = self.get_from_label()
            message = self.get_payload()
            # print ("this server received:" + message +" from: "+ new_to_label)
            
            if self.get_identifier()=="key_request" :
                
                #set attribute of output packet:
                public_key = self.get_pubic_key(shared_keys)
                self.to_label = new_to_label
                self.from_label = mylabel
                self.identifier = "ack_key_request"
                self.seqnum = self.seqnum
                self.payload = public_key.hex()

                to_link_layer = self.format_to_link_layer()

                return to_link_layer

            elif self.get_identifier()=="ack_key_request" :
                public_key = bytes.fromhex(message)
                shared_keys[new_to_label] = public_key
                return None

            elif self.get_identifier() == "message":
                message = self.message_decrypt(message,shared_keys)
                print ("decrypt message:" + message +" from: "+ new_to_label)

                #set ACK message attribute
                self.to_label = new_to_label
                self.from_label = mylabel
                self.identifier = "ACK"
                self.seqnum = self.seqnum
                self.payload = "ACK"
                to_link_layer = self.format_to_link_layer()
                return to_link_layer

            elif self.get_identifier() == "ACK" :
                return None

            else:
                return None # default action

        else: #not match keep sending message
            return self.get_forward_message()
    
    # support functions (method that can be change): 
    def get_pubic_key(self,shared_keys):
        ke2 = KeyExchange()
        ke2_public = ke2.ack_key_exchange_payload(self.from_label, shared_keys, bytes.fromhex(self.payload))
        # print("shared key create:", shared_keys[self.from_label])
        # print("return public key:", ke2_public)
        return ke2_public

    def message_decrypt(self,message,shared_keys):
        #print("message decrypt")
        shared_key = shared_keys.get(str(self.from_label), None)
        shared_keys.pop(self.from_label) 

        #print("message_decrypt", shared_key)
        # delete key after exchange
        cipher = SymmetricEncryption(shared_key)
        #print(bytes.fromhex(message))
        plaintext = cipher.decrypt(bytes.fromhex(message))
        #print(plaintext)
        return plaintext.decode()

    def format_to_link_layer(self):
        return self.to_label+","+self.from_label+","+self.identifier+","+self.seqnum+","+self.payload
    
    def get_forward_message(self):
        return self.forward_message

    def match_label(self, mylabel):
        
        return self.to_label == mylabel
    
    def get_from_label(self):
        return self.from_label

    def get_to_label(self):
        return self.to_label
        
    def get_payload(self):
        return self.payload

    def get_identifier (self):
        return self.identifier