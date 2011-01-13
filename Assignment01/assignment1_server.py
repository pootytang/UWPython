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

    #Data should be an int followed by space followed by another int
    l = data.split(' ')
    val = 0
    for i in l:
        val = val + int(i)

    print 'connection from: %s:%d' % address
    print 'responding with: %d' % val
    client.send(str(val))
    client.close()
