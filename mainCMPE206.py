import threading
import argparse
from application import server_main
from application import client_main

parser = argparse.ArgumentParser(description='CMPE206 Application')
parser.add_argument('--command', nargs='?', choices=['traceroute', 'ping', 'message'], default='message')

# main process
mylabel = input("my label name:")
shared_keys = dict()

# call subprocess
t_one = threading.Thread(target=server_main.service, args=(mylabel, shared_keys))
t_two = threading.Thread(target=client_main.service, args=(mylabel, shared_keys))
# exec subprocess
t_one.start()
t_two.start()

# wait thread process to end
t_one.join()
t_two.join()

print("Exit Service.")
