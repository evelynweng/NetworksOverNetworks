from data_parse.network_message import NetworkMessage


class Traceroute_service():
    def traceroute_send_service(self, mylabel, to_label):
        msg = NetworkMessage() \
            .set_from_label(mylabel).set_to_label(to_label) \
            .set_identifier('traceroute').set_acknowledgment_number('SYNC')\
            .set_sequence_number(1).set_start_time_now().set_ttl(1).set_to_label_original(to_label)
        return msg.get_data()
