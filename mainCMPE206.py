import threading
import os
from application import server_main 
from application import client_main

# main process
mylabel = input("my label name:")
ackflag = 0

# call subprocess
t_one = threading.Thread(target = server_main.service, args = (mylabel,))
t_two = threading.Thread(target = client_main.service, args = (mylabel,))
# exec subprocess
t_one.start()
t_two.start()



# wait thread process to end
t_one.join()
t_two.join()

print("Exit Service.")