class Find_to_mac():
    def find_mac(self, to_label):
      
        # import connection
        # only connection now eve<->evelyn<->kitty
        link_config = {}
        
        with open("link/configure_of_connection.txt") as configure_of_conneciton:
            for line in configure_of_conneciton:
                s = line.split(",")
                link_config[s[0]] = s[1][:-1]
        
        
        to_mac = link_config[to_label]
        
        return to_mac