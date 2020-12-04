import yaml

TOPOLOGY = 'sequential_topology'

class Find_to_mac():
    def __init__(self):
        with open("link/connection_config.yaml") as fl:
            self.config = yaml.full_load(fl)[TOPOLOGY]
    
    def get_my_mac(self):
        return "0.0.0.0"

    def find_mac(self, to_label):
        # import connection
        # only connection now eve<->evelyn<->kitty
        to_label = to_label.lower()
        if to_label not in self.config['global_routing_table']:
            return None
        direction = self.config['global_routing_table'][to_label]
        if direction not in self.config['left_right_neighbors']:
            return None
        
        return self.config['left_right_neighbors'][direction]
