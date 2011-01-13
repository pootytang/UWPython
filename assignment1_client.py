# Client side for assignment 1

import socket 

host = 'localhost'
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
s.send('Hello, world') 
data = s.recv(size) 
print 'Received:', data
s.close()
