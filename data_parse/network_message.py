import datetime

# [to_label, from_label, identifier, get_acknowledgment_number,  ...]
class NetworkMessage:
    to_network_layer = ['to_label', 'from_label', 'identifier', 'acknowledgment_number', '']

    def __init__(self, to=''):
        if bool(to):
            self.from_string(to)

    def set_to_label(self, val):
        self.to_network_layer[0] = str(val)
        return self

    def set_from_label(self, val):
        self.to_network_layer[1] = str(val)
        return self

    def set_identifier(self, val):
        self.to_network_layer[2] = str(val)
        self.update_message_length()
        return self

    def set_acknowledgment_number(self, val):
        self.to_network_layer[3] = str(val)
        return self

    def get_to_label(self):
        return self.to_network_layer[0]

    def get_from_label(self):
        return self.to_network_layer[1]

    def get_identifier(self):
        return self.to_network_layer[2]

    def get_acknowledgment_number(self):
        return self.to_network_layer[3]

    def from_string(self, data_string):
        self.to_network_layer = data_string.split(',')
        return self

    def from_array(self, data_array):
        self.to_network_layer = data_array
        return self

    def get_data(self):
        return ','.join(self.to_network_layer)

    def is_my_label(self, my_label):
        return self.to_network_layer[0] == my_label

    def update_message_length(self):
        data_length = 5
        if self.get_identifier() == 'ping':
            data_length = 6
        elif self.get_identifier() == 'traceroute':
            data_length = 8
        for x in range(data_length - len(self.to_network_layer)):
            self.to_network_layer.append('')
    # ----------------- end of common logic  ----------------------------
    # below headers, payload should start from index 4 and above

    # message [..., payload]
    def get_message(self):
        return ",".join(self.to_network_layer[4:])

    def set_message_payload(self, val):
        self.to_network_layer[5] = str(val)
        return self

    # ping [..., sequenc, start_time]
    def get_sequence(self):
        return self.to_network_layer[4]

    def get_start_time(self):
        return ','.join(self.to_network_layer[5:])

    def set_sequence(self, val):
        self.to_network_layer[4] = 'seq = ' + str(val)
        return self

    def set_start_time(self, val):
        self.to_network_layer[5] = str(val)
        return self

    def set_start_time_now(self):
        self.to_network_layer[5] = str(datetime.datetime.now())
        return self

    def Average(self, lst):
        return sum(lst) / len(lst)

    # traceroute [..., sequence, start_time, ttl, original_to]
    def get_ttl(self):
        return int(self.to_network_layer[6])

    def set_ttl(self, val):
        self.to_network_layer[6] = str(val)
        return self

    def set_sequence_number(self, val):
        self.to_network_layer[4] = str(val)
        return self

    def get_sequence_number(self):
        return int(self.to_network_layer[4])

    def get_start_time_value(self):
        return self.to_network_layer[5]

    def set_to_label_original(self, val):
        self.to_network_layer[7] = str(val)
        return self

    def get_to_label_original(self):
        return self.to_network_layer[7]
