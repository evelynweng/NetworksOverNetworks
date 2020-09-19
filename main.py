import threading
import os
from communication.udp_client import Client
from communication.udp_server import Server
import tkinter as tk






def send_message_gui():
    
    def submit():
        message_string = message.get()
        ip_address_string = ip_address.get()
        port_string = port.get()
        client = Client()
        client.udp_client(ip_address_string, port_string, message_string)

    master = tk.Tk()

    message_string = tk.StringVar()
    ip_address_string = tk.StringVar()
    port_string = tk.StringVar()


    

    tk.Label(master, text="IP Address to Send").grid(row=0)
    tk.Label(master, text="Port to Send").grid(row=1)
    tk.Label(master, text="Message").grid(row=2)
    message = tk.Entry(master, textvariable = message_string)
    ip_address =tk.Entry(master, textvariable = ip_address_string) 
    port =tk.Entry(master, textvariable = port_string) 

    ip_address.grid(row=0, column=1)
    port.grid(row=1, column=1)
    message.grid(row=2, column=1)

    send=tk.Button(master,text = 'Send', 
                      command = submit)
    send.grid(row=3, column=1)
    master.mainloop()



    

client = Client()
server = Server()
# main process
#mylabel = input("my label name:")
#ackflag = 0

# call subprocess
t_one = threading.Thread(target = server.udp_server, args = ())
t_two = threading.Thread(target = send_message_gui, args = ())
# exec subprocess
t_one.start()
t_two.start()



# wait thread process to end
t_one.join()
t_two.join()

print("Exit Service.")