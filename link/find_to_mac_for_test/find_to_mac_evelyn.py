class Find_to_mac():
    def find_mac(self, to_label):
    
        # import connection
        # only connection now eve<->evelyn<->kitty
        link_config = []
        '''
        with open("configure_of_conneciton.txt") as configure_of_conneciton:
            for line in configure_of_conneciton:
                s = line.split(",")
                link_config.append((s[0], s[1][:-1]))  # endl at the end
        '''
        if to_label == "kitty":
            # pass to kitty
            to_mac = "54.193.65.25"
        else:
            to_mac = "18.144.24.15"
        return to_mac