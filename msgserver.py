#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import threading
import time

ALL_CLIENT = []

# Define tcp handler for a thread...
def myHandler(client, addr):
    global ALL_CLIENT
    client.setblocking(0)
    ALL_CLIENT.append({
        'fd': client,
        'addr': addr,
        'closed': False
    });

    data=''
    while True:
        # avoid cpu loading too hight
        time.sleep(0.001)
        try:
            msg = client.recv(2)
            data += msg.decode(encoding='UTF-8', errors='ignore')
        except socket.error as e:
            if data != '':
                print('Server Recv: ', [data])
                for fd in ALL_CLIENT:
                    if fd['fd'] == client:continue
                    try:
                        fd['fd'].send(data.encode(encoding='UTF-8', errors='ignore'))
                    except Exception as e:
                        # This client raise error, so close it.
                        print('Server get a error fd: ', e)
                        fd['closed'] = True
                        # To remove /proc/$pid/fd/$clientfdFile
                        fd['fd'].close()

                # filter no use client
                ALL_CLIENT = [fd for fd in ALL_CLIENT if fd['closed'] == False]                
                data=''
            continue
        except Exception as e:
            print('Server get a error fd: ', e)
            break
    client.close()

# To launch Socket Server
server = socket.socket()
host = socket.gethostname()
port = 5200
server.bind(('0.0.0.0', port))
server.listen(5)
print('Server FD No: ', server.fileno())

while True:
    try:
        client, addr = server.accept()
        print('Got connection from', addr)
        threading.Thread(target=myHandler, args=(client, addr)).start()
    except KeyboardInterrupt:
        print('exit server.')
        client.close()
        for fd in ALL_CLIENT:fd['fd'].close()
        break
