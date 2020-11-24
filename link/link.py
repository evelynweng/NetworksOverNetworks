from link.find_to_mac import Find_to_mac
class Link():

    # outgoing packet format : link_identifier + to_mac + from_mac
    # from_mac is public IP of the running VM, need to get from initial server

    def __init__(self, to_link_layer = ""):
        self.temp_mac = "0.0.0.0"
        
        if to_link_layer: # data is from network layer 
            network_data = to_link_layer.split(",")
            self.to_label = network_data[0] #get to_label
            self.payload  = to_link_layer
        
        self.link_identifier = "CMPE206"
    
    def link(self):
        to_mac = self.find_next_mac()
        to_physical_layer = self.add_header_to_message()
        return to_mac , to_physical_layer

    def find_next_mac(self):
        # find to_mac
        find_to_mac = Find_to_mac()
        to_mac = find_to_mac.find_mac(self.to_label)
        return to_mac
    
    def find_my_mac(self):
        find_to_mac = Find_to_mac()
        my_mac = find_to_mac.get_my_mac()
        return my_mac

    def add_header_to_message (self):
        # outgoing packet format : link_identifier + to_mac + from_mac
        to_mac = self.find_next_mac()
        from_mac = self.find_my_mac()
        to_physical_layer = (self.link_identifier + "," + to_mac + "," 
                    + from_mac +"," + self.payload)
        return to_physical_layer
    
    def recv_message (self, receive_message): #de header

        if receive_message:
            message_data = receive_message.split(",")
            link_identifier = message_data[0]
            if link_identifier == "CMPE206":  #valid identifier->proceed
                to_network_layer = ','.join(message_data[3 : ])
                return to_network_layer
            else:
                return None
        else:
            return None
        
    


