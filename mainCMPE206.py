import threading
import argparse
from application import server_main
from application import client_main

parser = argparse.ArgumentParser(description='CMPE206 Application')
parser.add_argument("--traceroute", nargs='?', const=True, default=False)
parser.add_argument("--ping", nargs='?', const=True, default=False)
parser.add_argument('--command', nargs='?', choices=['traceroute', 'ping', 'message'], default='message')

args = parser.parse_args()
print(args)


# main process
mylabel = input("my label name:")
ackflag = 0

# call subprocess
t_one = threading.Thread(target=server_main.service, args=(mylabel,))
t_two = threading.Thread(target=client_main.service, args=(mylabel,))
# exec subprocess
t_one.start()
t_two.start()

# wait thread process to end
t_one.join()
t_two.join()

print("Exit Service.")
