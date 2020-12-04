import threading, queue
import argparse
from application import server_main
from application import client_main
from application import send_main

parser = argparse.ArgumentParser(description='CMPE206 Application')
parser.add_argument('--command', nargs='?', choices=['traceroute', 'ping', 'message'], default='message')

# main process
mylabel = input("my label name:")
shared_keys = dict()
recv_shared_keys = dict()
Tx_queue = queue.Queue()



# call subprocess
t_server = threading.Thread(target=server_main.service, 
                            args=(mylabel, shared_keys,Tx_queue,recv_shared_keys))
t_send = threading.Thread(target=send_main.service, args=(mylabel,Tx_queue))
t_app_client = threading.Thread(target=client_main.service, 
                            args=(mylabel,shared_keys,Tx_queue,recv_shared_keys))

# exec subprocess
t_server.start()
t_send.start()
t_app_client.start()

# wait thread process to end
t_server.join()
t_send.join()
t_app_client.join()

print("Exit Service.")
