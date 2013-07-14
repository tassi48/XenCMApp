#!/usr/bin/python

import threading
import time
import socket               # Import socket module
import os
import pickle

class myThread (threading.Thread):
	def __init__(self, clientsock, addr, name, delay):
		threading.Thread.__init__(self)
		self.clientsock = clientsock
		self.addr = addr
		self.name = name
		self.delay = delay
		
	
	def run(self):
		
		print "Starting " + self.name
		# Get lock to synchronize threads
		threadLock.acquire()
		get_data(self)
		# Free lock to release next thread
		threadLock.release()
		threads.remove(self.clientsock)

def get_data(self):
    	
	self.clientsock.send('s')
	data = self.clientsock.recv(BUFSIZ)
	dic = pickle.loads(data)
	
	print dic
	#print self.clientsock
	#print self.addr[0]
	machines[self.addr[0]] = dic
	#self.clientsock.send('b')
	
def start_threads() :
	
	

class analyzer (threading.Thread):
	def __init__(self, threadID, name ):
		threading.Thread.__init__(self)
		self.threadID = threadID
        	self.name = name
		
	
	def run(self):
		print "Starting " + self.name
		j = 1
		while 1 :
			while len(clients) < 2 :
				time.sleep(5)
				 
			
			#start all threads
			threadLock.acquire()
			for c in clients :
				thread = myThread(c[0], c[1], "ChildThread", 5)
				threads.append(c[0])
				thread.start()
			threadLock.release()
		
		
		
			#Wait for Childs to get data
		
			while len(threads) > 0  :
				time.sleep(5)
			
			#Analyze
			threadLock.acquire()
			maximum = 0.0
			minimum = 100.0
			
			for items in machines :
				summ = 0.0
				print "Hello", items
				print machines[items]
				for i in machines[items] :
					summ += machines[items][i][1]
			
				if summ > maximum :
					maximum = summ
					max_addr = items
				if summ < minimum :
					minimum = summ
					min_addr = items
			
			print 'MAXIMUM :', maximum, '  MINIMUM :' ,minimum
			actual_diff = 100
			#check if source machin has more than 1 domain
			if len(machines[max_+addr]) > 2 :
				
				for i in machines[max_addr] :
					if i != 'Domain-0' :
						temp1 = maximum - machines[max_addr][i][1]
						temp2 = minimum + machines[max_addr][i][1]
						diff = temp1 - temp2
						if diff < 0 :
							diff *= -1
					
						if diff < actual_diff :
							actual_diff = diff
							domain_id = machines[max_addr][i][0]
						
					else : 
						print 'condition checked'
					
				print 'Machine to be Migrated :', max_addr, '  ', domain_id
				verify()
			
			threadLock.release()
			j += 1
			time.sleep(30)


threadLock = threading.Lock()
threads = []

HOST = ''
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(5)
machines={}

thread1 = analyzer(1, "Analyzer")
thread1.start()
#threads.append(thread1)
clients = []

while True :
	print 'waiting for connections'
	clientsock, addr = serversock.accept()
	threadLock.acquire()
	clients.append([clientsock, addr])
	#thread = myThread(clientsock, addr, "ChildThread", 5)
	#threads.append(thread)
	print 'connected from:', addr
	threadLock.release()




# Wait for all threads to complete
#for t in threads:
#   t.join()
#print "Exiting Main Thread"
