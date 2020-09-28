from link.find_to_mac import Find_to_mac
class Link():
    def __init__(self):
        self.temp_mac = "0.0.0.0"

    def find_next_mac(self, to_link_layer):
        # find to_label
        to_label_end = to_link_layer.find(",")
        to_label = to_link_layer[:to_label_end]
        
        # find to_mac
        find_to_mac = Find_to_mac()
        to_mac = find_to_mac.find_mac(to_label)

        return to_mac

    def add_header_to_message (self,to_link_layer):
        to_mac = self.find_next_mac(to_link_layer)
        return to_mac+','+to_link_layer
    
    def de_header_receive_message (self, receive_message):
        print(type(receive_message), receive_message)
        to_mac_end = receive_message.find(",")
        to_network_layer = receive_message[to_mac_end+1:]
        return to_network_layer
        
    


