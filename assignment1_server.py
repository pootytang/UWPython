#  Server that expects 2 numbers and will respond with the sum of those numbers

import socket 
import time

host = 'localhost' 
port = 50000 
backlog = 5 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog)
while True: 
    client, address = s.accept()
    data = client.recv(size) 
    print data
    client.close()
