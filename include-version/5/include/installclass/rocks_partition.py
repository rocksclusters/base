#!/opt/rocks/bin/python
#
#
# LC
#
# Centos 5 (differently from Centos 6) does not support booting on a GPT 
# partition table:
# https://access.redhat.com/knowledge/solutions/15224
# it can use GPT partition for other disk though
# 

import syslog
import string
import os
import re
import tempfile
import sys
sys.path.append('/usr/lib/anaconda')
sys.path.append('/usr/lib64/python2.4/site-packages')
sys.path.append('/usr/lib/python2.4/site-packages')
import isys

import time

class RocksPartition:
	saved_fstab = []
	raidinfo = ''
	mountpoints = []

	def getDisks(self):
		disks = []
		file = open('/tmp/discovered.disks', 'r')
		for line in file.readlines():
			l = string.split(line)
			if len(l) > 0 and l[0] == 'disks:':
				for d in l[1:]:
					#
					# only include disks that have their
					# 'media present' -- this is one way
					# to filter out Dell Virtual Floppy
					# devices
					#
					if isys.mediaPresent(d):
						disks.append(d)

		file.close()

		return disks

	def getRaids(self):
		raids = []
		file = open('/tmp/discovered.disks', 'r')
		for line in file.readlines():
			l = string.split(line)
			if len(l) > 0 and l[0] == 'raids:':
				raids = l[1:]
		file.close()

		return raids

	def gptDrive(self, devname):
		#
		# if this is a drive with a GPT format, then return '1'
		#
		retval = 0

		cmd = '%s /dev/%s print -s 2> /dev/null' % \
			(self.parted, devname)

		label = 'Partition Table:'
		for line in os.popen(cmd).readlines():
			if len(line) > len(label) and \
				line[0:len(label)] == label:

				l = string.split(line)
				if len(l) > 2 and l[2] == 'gpt':
					retval = 1
					break

		return retval


	def getDevice(self, str):
		device = ''

		a = string.split(str, '/dev/')
		if len(a) > 1:
			device = a[1]

		return string.strip(device)


	def getSectorStart(self, str):
		sectorstart = ''

		a = string.split(str, '=')
		if len(a) > 1 and string.strip(a[0]) == 'start':
			sectorstart = a[1]
		else:
			sectorstart = a[0]

		return string.strip(sectorstart)


	def getPartitionSize(self, str):
		partitionsize = ''

		a = string.split(str, '=')
		if len(a) > 1 and string.strip(a[0]) == 'size':
			partitionsize = a[1]
		else:
			partitionsize = a[0]

		return string.strip(partitionsize)


	def getPartId(self, str):
		partid = ''

		a = string.split(str, '=')
		if len(a) > 1 and string.strip(a[0]) == 'Id':
			partid = a[1]
		else:
			partid = a[0]
		
		return string.strip(partid)


	def getFsType(self, mntpoint):
		return self.findFsTypeInFstab(mntpoint)


	def getBootFlags(self, str):
		return string.strip(str)
		

	def getMountPoint(self, devicename):
		mntpoint = self.findMntInFstab('/dev/' + devicename)
		
		if mntpoint == '':
			#
			# see if the device is part of a raidset
			#
			mntpoint = self.getRaidName(devicename)

		if mntpoint == '':
			cmd = '%s /dev/%s 2> /dev/null' % \
				(self.e2label, devicename)
			label = os.popen(cmd).readlines()

			label = string.join(label)
			id = 'LABEL=%s' % (label[:-1])

			mntpoint = self.findMntInFstab(id)

		return mntpoint


	def getRaidName(self, partition_device):
		raidname = ''

		for info in self.raidinfo:
			if len(info) > 3:
				(device, partitions, raidlevel,
					num_partitions) = info

				if partition_device in partitions:
					raidname = 'raid.%s' % partition_device
					break

		return raidname


	def findMntInFstab(self, identifier):
		for line in self.saved_fstab:
			l = string.split(line)
			if len(l) > 0:
				if l[0] == identifier:
					return l[1]

		return ''


	def findFsTypeInFstab(self, mntpoint):
		for line in self.saved_fstab:
			l = string.split(line)
			if len(l) > 2:
				if l[1] == mntpoint:
					return l[2]

		return ''


	def formatPartedNodePartInfo(self, devname, info):
		#
		# this function parses partition info from 'parted'
		#
		partinfo = []
		isDisk = 0
		
		for line in info:
			l = string.split(line[:-1])

			if len(l) > 2 and re.match('[0-9]+', l[0]):
				if devname[0:2] == 'md':
					device = devname
				elif len(devname) > 4 and \
						devname[0:5] == 'cciss':
					#
					# special case for HP smart array
					# controllers
					#
					device = devname + 'p' + l[0]
				else:
					device = devname + l[0]
				isDisk = 1
			else:
				if len(l) > 1 and l[0] == 'Disk':
					isDisk = 1
				continue

			sectorstart = l[1]
			partitionsize = l[3]
			partid = ''
			
			if devname[0:2] == 'md' and len(l) > 4:
				#
				# special case for software RAID. there is
				# no 'Type' or 'Flags' fields, so the
				# 'File system' field is 5th field
				#
				fstype = l[4]
				bootflags = ''
			else:
				bfs = None	
				if len(l) > 5 and not self.gptDrive(devname):
					#
					# there is a case for RAID 0 that the 
					# second partition of the drive does not
					# get the file system label (e.g., ext3), so
					# the 'boot flags' get misidentified as a
					# file system type
					#
					if 'raid' in l[5] or 'boot' in l[5]:
						bfs = l[5:]
						fstype = ''
					
					else:
						fstype = l[5]
				else:
					fstype = ''
			
					if len(l) > 4 and self.gptDrive(devname):
						# gpt partition there is not 
						# Type column so fstype is in 4 
						fstype = l[4]
						if len(l) > 5:
							bfs = [l[5]]
					

				if not bfs and len(l) > 6:
					bfs = l[6:]

				if bfs:
					bf = []                                         
					for b in bfs:
						bf.append(b.rstrip(','))                
					bootflags = ' '.join(bf)  
				else:
					bootflags = ''

			if fstype == 'linux-swap':
				mntpoint = 'swap'
			else:
				mntpoint = self.getMountPoint(device)

			# print 'formatPartedNodePartInfo:l: ', l

			partinfo.append('%s,%s,%s,%s,%s,%s,%s,%s\n' %
					(device, sectorstart, partitionsize,
						partid, fstype, bootflags, '',
								mntpoint))

		# print 'formatPartedNodePartInfo:partinfo: ', partinfo

		if partinfo == [] and isDisk:
			#
			# this disk has no partitions, create a
			# dummy null entry for it
			#
			partinfo = [ '%s,,,,,,,\n' % (devname) ]

		return partinfo


	def parsePartInfo(self, info):
		n = string.split(info, ',')

		if len(n) != 8:
			return ('', '', '', '', '', '', '', '')

		device = string.strip(n[0])
		sectorstart = string.strip(n[1])
		partitionsize = string.strip(n[2])
		partid = string.strip(n[3])
		fstype = string.strip(n[4])
		bootflags = string.strip(n[5])
		partflags = string.strip(n[6])
		mntpoint = string.strip(n[7])

		return (device, sectorstart, partitionsize, partid, 
			fstype, bootflags, partflags, mntpoint)


	def getDiskInfo(self, disk):
		syslog.syslog('getDiskInfo: disk:%s' % (disk))

		cmd = '%s /dev/%s ' % (self.parted, disk)
		cmd += 'print -s 2> /dev/null'
		diskinfo = os.popen(cmd).readlines()
		
		syslog.syslog('getNodePartInfo: diskinfo:%s' % (diskinfo))

		return diskinfo


	def getRaidLevel(self, device):
		level = None

		cmd = '%s --query --detail ' % (self.mdadm)
		cmd += '/dev/%s' % (device)
		for line in os.popen(cmd).readlines():
			l = line.split()
			if len(l) > 3 and l[0] == 'Raid' and l[1] == 'Level':
				if l[3][0:4] == 'raid':
					level = l[3][4:]
					break
		
		return level


	def getRaidParts(self, device):
		parts = []

		foundparts = 0
		cmd = '%s --query --detail ' % (self.mdadm)
		cmd += '/dev/%s' % (device)
		for line in os.popen(cmd).readlines():
			l = line.split()
			if len(l) > 4 and l[3] == 'RaidDevice':
				foundparts = 1
				continue

			if foundparts == 0:
				continue

			if len(l) == 0:
				continue
			
			part = l[-1].split('/')
			parts.append('raid.%s' % part[-1])

		return ' '.join(parts)

	
	def getNodePartInfo(self, disks):
		arch = os.uname()[4]

		partinfo = []
		nodedisks = {}

		# print 'getNodePartInfo:disks ', disks
		#
		# try to get the 
		#
		for line in self.getFstab(disks):
			self.saved_fstab.append(line)

		for devname in disks:
			diskinfo = self.getDiskInfo(devname)
			partinfo += self.formatPartedNodePartInfo(devname,
				diskinfo)

		syslog.syslog('getNodePartInfo: partinfo:%s' % (partinfo))

		for node in partinfo:
			n = self.parsePartInfo(node)

			(nodedevice, nodesectorstart, nodepartitionsize,
				nodepartid, nodefstype, nodebootflags,
				nodepartflags, nodemntpoint) = n

			if (len(nodedevice) > 2) and (nodedevice[0:2] == 'md'):
				nodepartflags = '--level=%s' % \
					self.getRaidLevel(nodedevice)

				nodebootflags = self.getRaidParts(nodedevice)

				n = (nodedevice, nodesectorstart,
					nodepartitionsize,
					nodepartid, nodefstype,
					nodebootflags,
					nodepartflags, nodemntpoint)

			elif nodebootflags != '':
				if 'raid' in nodebootflags.split():
					nodemntpoint = 'raid.%s' % (nodedevice)

					n = (nodedevice, nodesectorstart,
						nodepartitionsize,
						nodepartid, nodefstype,
						nodebootflags,
						nodepartflags, nodemntpoint)
				
			if nodedevice != '':
				key = ''
				for disk in disks:
					if len(disk) <= len(nodedevice) and \
						disk == nodedevice[0:len(disk)]:

						key = disk
						break

				if key != '':
					if not nodedisks.has_key(key):
						nodedisks[key] = [n]
					else:
						nodedisks[key].append(n)

		syslog.syslog('getNodePartInfo:nodedisks:%s' % (nodedisks))

		return nodedisks


	def listDiskPartitions(self, disk):
		list = []
		inHeader = 1
		
		if disk[0:2] == 'md':
			return [ (disk, 'dummy') ]

		for part in self.getDiskInfo(disk):
			l = string.split(part)

			#
			# skip the 'parted' header
			#
			if len(l) > 1 and l[0] == 'Number':
				inHeader = 0
				continue

			if inHeader:
				continue

			partnumber = 0

			#
			# look for a part number
			#
			if len(l) > 2 and re.match('[0-9]+', l[0]):
				partnumber = int(l[0])

			if partnumber > 0:
				if len(disk) > 4 and disk[0:5] == 'cciss':
					#
					# special case for HP smart array
					# controllers
					#
					disk = disk + 'p'

				if len(l) > 5:
					fstype = l[5]
				else:
					fstype = ''
					if len(l) > 4 and self.gptDrive( disk ):
						# this is a gpt partition
						fstype = l[4]
						

				list.append(('%s%d' % (disk, partnumber),
					fstype))

		return list


	def defaultDataDisk(self, disk):
		basename = '/state/partition'
		parts = []

		i = 1
		while 1:
			nextname = '%s%d' % (basename, i)
			if nextname not in self.mountpoints:
				break
			i = i + 1

		p = 'part '
		p += '%s --size=1 ' % (nextname)
		p += '--fstype=ext3 --grow --ondisk=%s ' % (disk)
		self.mountpoints.append(nextname)
		parts.append(p)

		return parts


	def RocksGetPartsize(self, mountpoint):
		size = 0

		if mountpoint == 'root':
			size = 16000
		elif mountpoint == 'var':
			size = 4000
		elif mountpoint == 'swap':
			size = 1000

		return size


	def defaultRootDisk(self, disk):
		arch = os.uname()[4]
		parts = []

		if arch == 'ia64':
			p = 'part /boot/efi --size=1000 --fstype=vfat '
			p += '--ondisk=%s\n' % (disk)

		p = 'part '
		p += '/ --size=%d ' % (self.RocksGetPartsize('root'))
		p += '--fstype=ext3 --ondisk=%s ' % (disk)
		self.mountpoints.append('/')
		parts.append(p)

		p = 'part '
		p += '/var --size=%d ' % (self.RocksGetPartsize('var'))
		p += '--fstype=ext3 --ondisk=%s ' % (disk)
		self.mountpoints.append('/var')
		parts.append(p)

		p = 'part '
		p += 'swap --size=%d ' % (self.RocksGetPartsize('swap'))
		p += '--fstype=swap --ondisk=%s ' % (disk)
		self.mountpoints.append('swap')
		parts.append(p)

		#
		# greedy partitioning
		#
		parts += self.defaultDataDisk(disk)

		return parts


	def getFstab(self, disks):
		if os.path.exists('/upgrade/etc/fstab'):
			file = open('/upgrade/etc/fstab')
			lines = file.readlines()
			file.close()
			return lines

		#
		# if we are here, let's go look at all the disks for /etc/fstab
		#
		mountpoint = tempfile.mktemp()
		os.makedirs(mountpoint)
		fstab = mountpoint + '/etc/fstab'

		lines = []
		for disk in disks:
			for (partition, fstype) in \
					self.listDiskPartitions(disk):

				if not fstype or fstype == 'linux-swap':
					continue

				os.system('mount /dev/%s %s' \
					% (partition, mountpoint) + \
					' > /dev/null 2>&1')

				if os.path.exists(fstab):
					file = open(fstab)
					lines = file.readlines()
					file.close()

				os.system('umount %s 2> /dev/null' %
					(mountpoint))

				if len(lines) > 0:
					break

			if len(lines) > 0:
				break

		try:
			os.removedirs(mountpoint)
		except:
			pass

		return lines


	def isRocksDisk(self, partinfo, touchit = 0):
		retval = 0

		mountpoint = tempfile.mktemp()
		os.makedirs(mountpoint)

		for part in partinfo:
			(dev,start,size,id,fstype,bootflags,partflags,mnt) = \
				part

			if not fstype or fstype == 'linux-swap':
				continue

			devname = '/dev/%s' % (dev)

			os.system('mount %s %s' % (devname, mountpoint))

			try:
				filename = mountpoint + '/.rocks-release'

				if touchit == 1:
					os.system('touch %s' % filename)

				if os.path.exists(filename):
					retval = 1
			except:
				pass

			os.system('umount %s' % (mountpoint) +
				' > /dev/null 2>&1')

			if retval == 1:
				break

		try:
			os.removedirs(mountpoint)
		except:
			pass

		return retval


	def addPartitions(self, nodepartinfo, format):
		arch = os.uname()[4]
		parts = []

		#
		# for each partition on a drive, build a partition
		# specification for anaconda
		#
		for node in nodepartinfo:
			if len(node) == 1:
				continue

			(nodedevice, nodesectorstart, nodepartitionsize,
				nodepartid, nodefstype, nodebootflags,
					nodepartflags, nodemntpoint) = node

			if arch == 'ia64':
				if nodefstype == 'fat32':
					nodefstype = 'vfat'
				elif nodefstype == 'linux-swap':
					nodefstype = 'swap'

			if nodemntpoint == '':
				continue

			#
			# only add raid partitions if they have a mountpoint
			# defined by their respective 'md' device.
			#
			# anaconda will crash if there is not a valid
			# mountpoint for the md device
			#
			if nodepartid == 'fd':
				if not self.getRaidMountPoint(nodedevice):
					continue

			args = [ nodemntpoint ]

			if len(nodemntpoint) > 3 and \
						nodemntpoint[0:4] == 'raid':
				#
				# never format a software raid partition and
				# always set its size to 1
				# 
				args.append('--noformat')
				args += [ '--size', '1' ]
			elif (nodemntpoint != '/' and nodemntpoint != '/var') \
					and not format:
				args.append('--noformat')
			else:
				if nodefstype == '':
					args += [ '--fstype', self.fstype ]
				else:
					args += [ '--fstype', nodefstype ]

			israid = 0

			if len(nodedevice) > 2 and nodedevice[0:2] == 'md':
				israid = 1

				args += [ "--device=%s" % (nodedevice) ]

				if nodepartflags != '':
					args += [ nodepartflags ]

				for part in string.split(nodebootflags):
					if len(part) > 3 and \
							part[0:4] == 'raid':

						args.append(part) 
			else:
				args += [ "--onpart", nodedevice ]

			if israid:
				parts.append('raid %s' % (string.join(args)))
			else:
				parts.append('part %s' % (string.join(args)))

			self.mountpoints.append(nodemntpoint)

		return parts


	def compareDiskInfo(self, dbpartinfo, nodepartinfo):
		if len(dbpartinfo) != len(nodepartinfo):
			return 0

		for db in dbpartinfo:
			if len(db) == 1:
				continue
                
			(dbdevice, dbsectorstart, dbpartsize, dbpartid,
				dbfstype, dbbootflags, dbpartflags,
				dbmntpoint) = db
                
			found = 0
			for node in nodepartinfo:
				if len(node) == 1:
					continue
                        
				(nodedevice, nodesectorstart, nodepartsize,
					nodepartid, nodefstype, nodebootflags,
					nodepartflags, nodemntpoint) = node
                        
				# print 'compareDiskInfo:node: ', node
				# print 'compareDiskInfo:db: ', db

				if dbsectorstart == nodesectorstart and \
					dbpartsize == nodepartsize and \
					dbpartid == nodepartid and \
					dbfstype == nodefstype and \
					dbbootflags == nodebootflags and \
					dbpartflags == nodepartflags and \
					dbmntpoint == nodemntpoint:

					found = 1
					break
                        
			if not found:
				return 0
                        
		return 1


	def __init__(self):
		#
		# setup logging
		#
		syslog.openlog('ROCKS')

		#
		# setup path to commands
		#
		if os.path.exists('/mnt/runtime/usr/sbin/parted'):
			self.parted = '/mnt/runtime/usr/sbin/parted'
		else:
			self.parted = '/sbin/parted'

		if os.path.exists('/mnt/runtime/usr/sbin/e2label'):
			self.e2label = '/mnt/runtime/usr/sbin/e2label'
		else:
			self.e2label = '/sbin/e2label'

		if os.path.exists('/mnt/runtime/usr/sbin/mdadm'):
			self.mdadm = '/mnt/runtime/usr/sbin/mdadm'
		else:
			self.mdadm = '/sbin/mdadm'

		return

