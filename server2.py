#!/usr/bin/python

import threading
import time
import socket           # Import socket module
import os
import pickle		#support for Hash-table compression
import libvirt		#support for migration
import sys

#TODO
def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)


class myThread (threading.Thread):
	def __init__(self, clientsock, addr, name, delay):
		threading.Thread.__init__(self)
		self.clientsock = clientsock
		self.addr = addr
		self.name = name
		self.delay = delay
		self.kill_received = False
		
	
	def run(self):
		if not self.kill_received:
			print "Starting " + self.name + " For " + self.addr
			# Get lock to synchronize threads
			threadLock.acquire()
			get_data(self)
			# Free lock to release next thread
			threadLock.release()
			threads.remove(self.clientsock)
		
		if self.kill_received :
			self.clientsock.send('b')

def get_data(self):
    	self.clientsock.send('s')
	data = self.clientsock.recv(BUFSIZ)
	dic = pickle.loads(data)
	
	print dic
	#print self.clientsock
	#print self.addr[0]
	machines[self.addr[0]] = dic
	#self.clientsock.send('b')
	
	
#Start Threads
def start_threads() :
	while len(clients) < 2 :
		time.sleep(5)
		
	threadLock.acquire()
	for c in clients :
		thread = myThread(c[0], c[1], "ClientThread", 5)
		threads.append(c[0])
		thread.start()
	threadLock.release()
	

def analyze(self) :
	#start all threads
	start_threads()

	if not self.kill_received :
		#Wait for Childs to get data
		while len(threads) > 0  :
			time.sleep(5)
		#threadLock.acquire()
		maximum = 0.0
		minimum = 1000.0
	
		#Decision Phase
		for items in machines :
			summ = 0.0
			#print "Hello", items
			#print machines[items]
			for i in machines[items] :
				summ += machines[items][i][1]
	
			if summ > maximum :
				maximum = summ
				max_addr = items
			if summ < minimum :
				minimum = summ
				min_addr = items
	
		print 'MAXIMUM :', maximum, '  MINIMUM :' ,minimum
		prev_diff = maximum-minimum
		#threadLock.release()
		#Policy-1
		if prev_diff > DIFF_1 and not self.kill_received :
								
			#Location and Identification Phase
			current_diff = 1000 #Big_Interger
			#check if source machin has more than 1 domain
		
			#Policy-2.1
			if len(machines[max_addr]) > (MIN_VMS+1) and not self.kill_received :
		
				for i in machines[max_addr] :
					if i != 'Domain-0' and not self.kill_received :
						temp1 = maximum - machines[max_addr][i][1]
						temp2 = minimum + machines[max_addr][i][1]
						diff = temp1 - temp2
						if diff < 0 :
							diff *= -1
			
						if diff < current_diff :
							current_diff = diff
							domain_id = machines[max_addr][i][0]
							usage = machines[max_addr][i][1]
					#else : 
						#print 'condition checked Domain-0 not included'
			
				#Policy-2.2
				if usage > MIN_USAGE  and not self.kill_received :
					#Policy-3
					if current_diff < (prev_diff-NEG_LIMIT) and not self.kill_received :
				
						#print 'Machine with Domain-Id ', domain_id, ' to be Migrated from :', max_addr, ' to :', min_addr
						return max_addr, domain_id , min_addr
					else :
						print 'Policy-3 - Negative'
				else :
					print 'Policy-2.2 - Negative'
			else :
				print 'Policy-2.1 - Negative'
		else :
			print 'Policy-1 - Negative'
	addr = 0
	return addr, -1, addr

#Migration Thread
def migrate(source_addr, domain_id, dest_addr):
	#Connect to hypervisor
	uri = "xen+ssh://root@" + str(source_addr)
	print 'Source URI :', uri
	conn_s = libvirt.open(uri)
	if conn_s == None :
		print 'Failed to open connection to the Source hypervisor'
		return -1
		
	uri = "xen+ssh://root@" + str(dest_addr)
	print 'Destination URI :', uri
	conn_d = libvirt.open(uri)
	if conn_d== None :
		print 'Failed to open connection to the Destination hypervisor'
		return -1
	
	print "Connection to Hypervisors Built Successfully"
	
	#Verify if domain is active
	dom = conn_s.lookupByID(domain_id)
	if dom == None :
		print ' No running domain with domain-id ', domain_id
		return -1
		
	uri = "xenmigr://"+str(dest_addr)
	result = dom.migrateToURI(uri, 1|16, None, 0)
	if result == -1 :
		print "Domain Migration Failed"
		return -1
		
	return 1
	
	


#Analyzer Thread
class analyzer (threading.Thread):
	def __init__(self, threadID, name ):
		threading.Thread.__init__(self)
		self.threadID = threadID
        	self.name = name
		self.kill_received = False
	
	def run(self):
		
			print "Starting " + self.name
			#j = 1
			while 1 :
						
				#Analyze
				if self.kill_received :
					break
				source_addr, domain_id , dest_addr= analyze(self)
				print 'Machine to be Migrated analyzed previously :', source_addr, '  ', domain_id
				if self.kill_received :
					break
				if domain_id != -1 :
					time.sleep(10)
					s_addr, d_id, d_addr = analyze(self)
					if self.kill_received :
						break
					print 'Machine to be Migrated analyzed now :', s_addr, '  ', d_id
					if d_id != -1 :
						if source_addr == s_addr and domain_id == d_id and dest_addr == d_addr :
					
							print '--Machine with Domain-Id-- ', domain_id, ' to be Migrated from :', source_addr, ' to :', dest_addr
							if self.kill_received :
								break
							threadLock.acquire()
							if migrate(source_addr, domain_id, dest_addr) == 1 :
								print "Migration Successful"
								time.sleep(10)
							threadLock.release()
			
				#j += 1
				time.sleep(10)
			


#Global Structures
threads = []
machines={}
clients = []

#Global Varibles
DIFF_1 = 50	#Difference in CPU usage of Extreme Nodes
MIN_VMS = 1	#No. of minimum VMs running on Source host
MIN_USAGE = 40	#Minimum CPU usage for migrating VM
NEG_LIMIT = 20	#Minimum Load reducing limit


#Client - Server Initialisation
HOST = ''
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(5)

#Thread Lock 
threadLock = threading.Lock()

#Analzer thread
thread1 = analyzer(1, "Analyzer")
thread1.start()


#Handling Ctrl+c
#signal.signal(signal.SIGINT, signal_handler)
kill_received = False

while not kill_received :
	try:
		print 'waiting for connections'
		clientsock, addr = serversock.accept()
		threadLock.acquire()
		clients.append([clientsock, addr])
		#thread = myThread(clientsock, addr, "ChildThread", 5)
		#threads.append(thread)
		print 'connected from:', addr
		threadLock.release()
	except KeyboardInterrupt:
		print "Ctrl-c received! Sending kill to threads..."
		while len(threads) > 0  :
			time.sleep(5)
		thread1.kill_received = True
		kill_received = True
		thread1.join()

# Wait for all threads to complete
#for t in threads:
#   t.join()
#print "Exiting Main Thread"
