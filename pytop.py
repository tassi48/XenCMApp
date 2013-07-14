#Dear God, Please save our Asses

#!/usr/bin/python

import time
import os
import sys
import socket 
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '172.17.4.34'
port = 12345
print host

s.connect((host, port))
while 1 :
	command=s.recv(1024)
	if command[0] == 's' :

		#for i in range(0, 3) :
		table = {} 

		os.system('xm list > domain')

		file1 = open('domain','r')
		line = file1.readline()

		for line in file1.readlines() :
			words = line.split()
			if int(words[1]) < 20 :
				table[words[0]] = [int(words[1]), 0.0 ]
	



		#print table
		iterations = 3
		os.system('xentop -i '+ str(iterations) +' -d 1 -b > output')

		file2 = open('output','r')
		for line in file2.readlines() :
			words=line.split()

			if words[0] in table :

				table[words[0]][1] +=  float(words[3])

		#print table

		for items in table :
			table[items][1] /= iterations

		print table
		#print len(pickle.dumps(table))

		s.send(pickle.dumps(table))
	
	if command[0] == 'b' :
		break 	
#print s.recv(1024)
s.close
	



