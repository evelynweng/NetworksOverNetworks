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
        # for test case eve-->david(not exist)
        # return None==drop the package
        print("to_label before decideing mac:", to_label)
        if to_label ==  "evelyn" or to_label == "eve" :
            to_mac = "13.52.77.84"
        else:
            to_mac = "0.0.0.0"
        
        return to_mac