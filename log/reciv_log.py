import sys
import os
from datetime import datetime


class Log():

    """
     this class logs the info on packet received since we runing
     our server on ec2 backgound. we arent able to see the server infos only if we 
     connect through ssh.logging the packet received into a text file would be useful if
     we need to them 
    """

    def log(self, msg,client_info):
        timer = self.get_current_time()
        timestampStr = timer.strftime("%d-%b-%Y (%H:%M:%S)")
        log_msg = "a pakcet recvied from client " + client_info + " at " + timestampStr
        print(log_msg)
        f = open("../log/logs.text", "a")
        f.write(log_msg + "\n")
        f.close()
        

    def get_current_time(self):
        datetime.now(tz=None)
        dateTimeObj = datetime.now()
        return dateTimeObj
