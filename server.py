#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import pickle
import os
os.system('xm list > domain')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = '172.17.4.34' # Get local machine name
addr = socket.gethostbyname(host)
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print addr
s.listen(5)
i=0                 # Now wait for client connection.
while True:
  	c, addr = s.accept()     # Establish connection with client.
   	for i in range(10) :
		data = c.recv(1024)
		dic = pickle.loads(data)
		print dic
	print 'Got connection from', addr
	c.send('Thank you for connecting')
	c.close()                # Close the connection
