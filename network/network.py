from security.key_exchange import DiffieHellman, KeyExchange
from security.symmetric_encryption import SymmetricEncryption

import datetime
from dateutil.parser import parse
from data_parse.network_message import NetworkMessage

rtt_arr = []


def is_equal(str1, str2):
    return str1 == str2


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
            self.unchange_message = to_network_layer #packet unchange

    def network(self, to_network_layer):
        to_link_layer = to_network_layer
        return to_link_layer
    
    def recv_packet (self, mylabel,shared_keys):

        if self.match_label(mylabel):
            # print ("this server received:" + message +" from: "+ new_to_label)
            if self.get_identifier()=="key_request" :
                to_link_layer =self.function_key_request(mylabel,shared_keys)
                return to_link_layer
        
            elif self.get_identifier()=="ack_key_request" :
                to_link_layer = self.function_ack_key_request(shared_keys)
                return to_link_layer

            elif self.get_identifier() == "message":
                to_link_layer = self.function_message(mylabel,shared_keys)
                return to_link_layer

            elif self.get_identifier() == "ACK" :
                print("recv, ACK from:", self.get_from_label())
                return None
            
            elif self.get_identifier() == "ping":
                to_link_layer = self.function_ping(self.unchange_message,mylabel)
                return to_link_layer
            
            elif self.get_identifier() == "traceroute":
                to_link_layer = self.handle_traceroute(self.unchange_message, mylabel)
                return to_link_layer

            else:
                return None # default action

        elif self.get_identifier() == 'traceroute':
            to_link_layer = self.handle_traceroute_mid(self.unchange_message, mylabel)
            return to_link_layer

        else: #not match keep sending message
            print("forward message")
            return self.get_forward_message()


    # support functions (method that can be change):
    def handle_traceroute_mid(self, to_network_layer, mylabel):
        network_message = NetworkMessage().from_string(to_network_layer)
        new_to_label = network_message.get_from_label()
        response_network_message = NetworkMessage().from_string(to_network_layer).set_to_label(new_to_label) \
            .set_from_label(mylabel).set_acknowledgment_number('ACK')
    
        ttl = network_message.get_ttl()
        print("handle_traceroute_mid" + network_message.get_data())
        if ttl > 0:
            network_message = network_message.set_ttl(ttl - 1)
            return network_message.get_data()
        else:
            return response_network_message.set_ttl(15).get_data()

    def handle_traceroute(self, to_network_layer, mylabel):
        network_message = NetworkMessage().from_string(to_network_layer)
        new_to_label = network_message.get_from_label()
        response_network_message = NetworkMessage().from_string(to_network_layer).set_to_label(new_to_label) \
            .set_from_label(mylabel).set_acknowledgment_number('ACK')
        print("handle_traceroute" + network_message.get_data())
        if network_message.get_acknowledgment_number() == "ACK":
            start_time = network_message.get_start_time()
            end_time = datetime.datetime.now()
            rtt_datetime = end_time - parse(start_time)
            hop = network_message.get_sequence_number()
            hop_max = 15 - network_message.get_ttl() - hop
            print(' '.join(['hop #', 'rtt', 'name']))
            message = ' '.join([hop, str(rtt_datetime.total_seconds()), network_message.get_from_label(), hop_max])
            print(message)

            if is_equal(network_message.get_from_label(), network_message.get_to_label_original()):
                    print("End")
            else:
                response_network_message.set_to_label(network_message.set_to_label_original()).set_acknowledgment_number('SYNC')\
                    .set_sequence_number(network_message.get_sequence_number() + 1).set_start_time_now()\
                    .set_ttl(network_message.get_sequence_number() + 1)
                return response_network_message

            return None
        else:
            return response_network_message.set_ttl(15).get_data()

    def function_ping(self,to_network_layer,mylabel):
        network_message = NetworkMessage(to_network_layer)
        new_to_label = network_message.get_from_label()
        identifier = network_message.get_identifier()
        response_network_message = NetworkMessage(to_network_layer).set_to_label(new_to_label) \
            .set_from_label(mylabel).set_acknowledgment_number('ACK')

        if network_message.get_acknowledgment_number() == "ACK":
            sequence = network_message.get_sequence()
            start_time = network_message.get_start_time()
            end_time = datetime.datetime.now()

            rtt_datetime = end_time - parse(start_time)
            rtt_arr.append(rtt_datetime.total_seconds())
            network_layer_packet = to_network_layer.split(',')
            packet = network_layer_packet[:4]
            print("Ping Reply: " + ",".join(packet) + "," + 'rtt = ' + str(rtt_datetime.total_seconds()) + ' s')
            if len(rtt_arr) == 5:
                print("PING statistics")
                print("Avg rtt = ", network_message.Average(rtt_arr), "seconds")
                print("5 packets transmitted, 5 packets recieved")
                rtt_arr.clear()

            return None
        else:
            sequence = network_message.get_sequence()
            start_time = network_message.get_start_time()
            return response_network_message.set_sequence(sequence).set_start_time(start_time).get_data()

    def function_message(self,mylabel,shared_keys):
        new_to_label = self.get_from_label()
        message = self.get_payload()
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
    
    def function_key_request(self,mylabel,shared_keys):
        new_to_label = self.get_from_label()
        message = self.get_payload()
                #set attribute of output packet:
        public_key = self.get_pubic_key(shared_keys)
        self.to_label = new_to_label
        self.from_label = mylabel
        self.identifier = "ack_key_request"
        self.seqnum = self.seqnum
        self.payload = public_key.hex()
        to_link_layer = self.format_to_link_layer()
        return to_link_layer

    def function_ack_key_request(self,shared_keys):
        new_to_label = self.get_from_label()
        message = self.get_payload()

        public_key = bytes.fromhex(message)
        shared_keys[new_to_label] = public_key
        return None

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
        return self.unchange_message

    def match_label(self, mylabel):
        
        return (self.to_label) == mylabel
    
    def get_from_label(self):
        return self.from_label

    def get_to_label(self):
        return self.to_label
        
    def get_payload(self):
        return self.payload

    def get_identifier (self):
        return self.identifier