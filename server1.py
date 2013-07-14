#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import thread
import time
import os
import pickle



def handler(clientsock,addr):
	i=0
	while 1:
		
		if i == 2 :
			
			break
		lock.acquire()
		clientsock.send('s')
		data = clientsock.recv(BUFSIZ)
		#if not data: break
		dic = pickle.loads(data)
		print dic
		machines[[clientsock,addr]] = dic
		
		#clientsock.send('echoed: Thank you for connecting')
		i+=1
		lock.release()
		time.sleep(5)
		
	
	
	clientsock.close()


HOST = ''
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)
global lock
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(5)
lock = thread.allocate_lock()
machines={}


while True :
	print 'waiting for connections'
	clientsock, addr = serversock.accept()
	print 'connected from:', addr
	thread.start_new_thread(handler, (clientsock, addr))
#some other cleanup code if necessary


