import libvirt	

def migrate(source_addr, domain_id, dest_addr):
	#Connect to hypervisor
	uri = "xen+ssh://root@" + str(source_addr)
	print 'Source URI :', uri
	conn_s = libvirt.open(uri)
	if conn_s == None :
		print 'Failed to open connection to the Source hypervisor'
		return -1
		
	uri = "xen+ssh://root@" + str(dest_addr)
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
	
source_addr = '172.17.4.34'
domain_id = 1
dest_addr = '172.17.4.36'
if migrate(source_addr, domain_id, dest_addr) == 1 :
	print "Migration Successful"
	
