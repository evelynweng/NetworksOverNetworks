# ackflag = 0

class Network():
    def network(self, to_network_layer):
        #do nothing at this moment
        return to_network_layer
    
    def forward_message (self, mylabel, to_network_layer):
        print(__name__, mylabel, to_network_layer)
        if self.match_label(mylabel, to_network_layer):
            new_to_label = self.get_from_label(to_network_layer)
            message = self.get_payload(to_network_layer)
            print ("this server received:" + message +" from: "+ new_to_label)
            
            if message == "ACK" :
                # ackflag = 1
                return None
            else:
                return new_to_label+","+mylabel+","+"ACK"

        else: #not match keep sending message
            return to_network_layer
    
    # support functions (method that can be change): 

    def match_label(self, mylabel, to_network_layer):
        to_label_end = to_network_layer.find(",")
        to_label = to_network_layer[:to_label_end]
        return to_label == mylabel
    
    def get_from_label(self, to_network_layer):
        to_label_end = to_network_layer.find(",")
        from_label_message = to_network_layer[to_label_end+1:]
        from_label_end = from_label_message.find(",")
        from_label = from_label_message[:from_label_end]

        return from_label
        
    def get_payload(self, to_network_layer):
        to_label_end = to_network_layer.find(",")
        from_label_message = to_network_layer[to_label_end+1:]
        from_label_end = from_label_message.find(",")
        from_label = from_label_message[:from_label_end]
        message = from_label_message[from_label_end+1:]

        return message

