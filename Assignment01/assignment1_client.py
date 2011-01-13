# Client side for assignment 1

import socket 

host = 'localhost'
port = 50000
size = 1024

#get the input from the user
num1 = raw_input("Enter the first number: ")
num2 = raw_input("Enter the second number: ")
num = num1 + " " + num2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
s.send(num)
data = s.recv(size) 
print 'Received:', data
s.close()
