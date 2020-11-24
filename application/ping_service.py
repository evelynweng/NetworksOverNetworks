import datetime
from data_parse.network_message import NetworkMessage

class Ping_service():
    def ping_send_service(self, mylabel, to_label):
        to_network_layer = []
        for i in range(1, 6):
            msg = NetworkMessage() \
                .set_from_label(mylabel).set_to_label(to_label) \
                .set_identifier('ping').set_acknowledgment_number('SYNC')\
                .set_sequence(i).set_start_time(datetime.datetime.now())
            to_network_layer.append(msg.get_data())
        return to_network_layer


if __name__ == "__main__":
    # Do some unit test
    test = Ping_service()
    test.ping_service("abc", "def")
