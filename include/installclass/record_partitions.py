#!/opt/rocks/bin/python

import sys
sys.path.append('/tmp/product')
import rocks_partition
import httplib
import random
import time
import string
sys.path.append('/tmp')
import db_partition_info

def sendit(server, req, nodepartinfo):
	status = 0

	h = httplib.HTTPSConnection(server, key_file = None, cert_file = None)
	h.putrequest('GET', '/install/sbin/public/setDbPartitions.cgi')

	h.putheader('X-Rocks-PartitionInfo', repr(nodepartinfo))

	try:
		h.endheaders()
		response = h.getresponse()
		status = response.status
	except:
		#
		# assume the error occurred due to an
		# authorization problem
		#
		status = 403
		pass

	h.close()
	return status

#
# main
#
p = rocks_partition.RocksPartition()

#
# get the list of hard disks and software raid devices
#
disks = p.getDisks() + p.getRaids()
nodepartinfo = p.getNodePartInfo(disks)

#
# only try to report the partitions back to the frontend, if this isn't
# a frontend
#
file = open('/proc/cmdline', 'r')
args = string.split(file.readline())
file.close()

if 'frontend' not in args:
	random.seed(int(time.time()))

	for i in range(0, 5):
		status = sendit(db_partition_info.KickstartHost,
			'/install/sbin/public/setDbPartitions.cgi',
			nodepartinfo)
	
		if status == 200:
			break
		else:
			time.sleep(random.randint(0, 10))
		
#
# mark each disk as a 'rocks' disk -- this let's us know that we have
# 'seen' and configured this disk
#
for disk in nodepartinfo.keys():
	p.isRocksDisk(nodepartinfo[disk], touchit = 1)

