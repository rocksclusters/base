#!/opt/rocks/bin/python

import sys
import string
import rocks_partition
import os

isManual = 0
partscheme = None

if os.path.exists('/tmp/db_partition_info.py'):
	sys.path.append('/tmp')
	import db_partition_info

	dbpartinfo = db_partition_info.dbpartinfo
else:
	dbpartinfo = {}

if os.path.exists('/tmp/user_partition_info'):
	file = open('/tmp/user_partition_info', 'r')
	for line in file.readlines():
		l = string.split(line)
		if len(l) == 2 and l[0] == 'rocks':
			partscheme = l[1]
			break
	file.close()

if partscheme != None:
	os.remove('/tmp/user_partition_info')

if partscheme == 'manual':
	#
	# manual partitioning, touch a file and bail
	#
	os.system('touch /tmp/manual-partitioning')
	sys.exit(0)

#
# link into a class that has several disk helper functions
#
p = rocks_partition.RocksPartition()

if partscheme:
	#
	# only get a list of disks (no raid devices) when a partscheme is
	# defined. this is because none of our auto partition schemes do
	# anything with a raid device.
	#
	disks = p.getDisks()
else:
	#
	# get the list of hard disks and software raid devices
	#
	disks = p.getDisks() + p.getRaids()
	
	for disk in p.getRaids():
		os.system('raidstart /dev/%s' % disk)

#
# get partition info for all the disks
#
nodedisks = p.getNodePartInfo(disks)

#
# save nodedisks in a temporary variable. if we have a match
# in the loop below, we can delete an entry from 'i' and not
# corrupt nodedisks while will loop over nodedisks's entries
#
i = nodedisks

parts = []

#
# reconnect all rocks disks (only if this is a non-frontend machine)
#
file = open('/proc/cmdline', 'r')
args = string.split(file.readline())
file.close()

if 'build' not in args:
	for disk in nodedisks.keys():
		if p.isRocksDisk(nodedisks[disk]):
			parts += p.addPartitions(nodedisks[disk], format = 0)

			#
			# this disk is recognized, so remove it from
			# nodedisks and disks
			#
			del i[disk]
			disks.remove(disk)
		
	nodedisks = i

#
# reconnect all disks that match in the database
#
for disk in nodedisks.keys():
	if dbpartinfo.has_key(disk) and \
		p.compareDiskInfo(dbpartinfo[disk], nodedisks[disk]):

		parts += p.addPartitions(nodedisks[disk], format = 0)

		#
		# this disk is recognized, so remove it from
		# nodedisks and disks
		#
		del i[disk]
		disks.remove(disk)

#
# get the user partitioning info
#
douserpartitioning = 0
if os.path.exists('/tmp/user_partition_info'):
	#
	# only do user partitioning if we *didn't* reconnect *any* of the disks
	#
	if len(parts) == 0:
		douserpartitioning = 1

		file = open('/tmp/user_partition_info', 'r')
		for line in file.readlines():
			parts.append(line[:-1])
		file.close()
else:
	installdisks = []
	if partscheme == 'force-default-root-disk-only':
		#
		# if we haven't found a root disk yet, then make the first
		# unrecognized disk the root disk
		#
		if '/' not in p.mountpoints and len(disks) > 0:
			installdisks.append(disks[0])
	elif partscheme == 'force-default':
		#
		# partition and format all unrecognized drives
		#
		installdisks = disks

	if len(installdisks) > 0:
		print 'clearpart --all --initlabel --drives=%s' % \
			(string.join(installdisks, ','))

	for disk in installdisks:
		if '/' not in p.mountpoints:
			parts += p.defaultRootDisk(disk)
		else:
			parts += p.defaultDataDisk(disk)

raid = []
raidparts = []
for line in parts:
	if line[0:4] == 'raid':
		raid.append(line)
	else:
		print line
	
if douserpartitioning == 0:
	for line in raid:
		#
		# if a physical partition specification for this software RAID
		# doesn't exist, then we need to create one
		#
		l = line.split()
		for i in range(len(l) - 1, -1, -1):
			if len(l[i]) > len('raid') and l[i][0:4] == 'raid':
				if l[i] not in p.mountpoints:
					a = l[i].split('.')
					if len(a) > 1:
						part = 'part %s --noformat ' \
							% l[i]
						part += '--size 1 --onpart %s' \
							% a[1]
					
						raidparts.append(part)
				
for line in raidparts:                                                              
	print line 
		
for line in raid:
	print line

