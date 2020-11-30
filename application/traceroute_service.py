from data_parse.network_message import NetworkMessage


class Traceroute_service():
    def traceroute_send_service(self, mylabel, to_label):
        to_network_layer = []
        for i in range(1, 12):
            msg = NetworkMessage() \
                .set_from_label(mylabel).set_to_label(to_label) \
                .set_identifier('traceroute').set_acknowledgment_number('SYNC')\
                .set_sequence_number(i).set_start_time_now().set_ttl(i).set_to_label_original(to_label)
            to_network_layer.append(msg.get_data())
        return to_network_layer
