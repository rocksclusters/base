#!/opt/rocks/bin/python
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: vm.py,v $
# Revision 1.7  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.6  2008/08/22 23:26:38  bruno
# closer
#
# Revision 1.5  2008/04/16 19:11:31  bruno
# only get partition info for partitions that are mountable (i.e., they
# have a leading '/' in the mountpoint field).
#
# Revision 1.4  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.3  2008/02/12 00:15:39  bruno
# partition sizes can be reported as floats
#
# Revision 1.2  2008/02/07 20:10:32  bruno
# added some global functions for VM management
#
# Revision 1.1  2008/01/31 20:05:32  bruno
# needed a helper function for the VM configuration rocks command line
#
#

import os
import sys


class VM:

	def __init__(self, db):
		self.db = db
		return


	def partsizeCompare(self, x, y):
		xsize = x[0]
		ysize = y[0]

		suffixes = [ 'KB', 'MB', 'GB', 'TB', 'PB' ]

		xsuffix = xsize[-2:].upper()
		ysuffix = ysize[-2:].upper()

		try:
			xindex = suffixes.index(xsuffix)
		except:
			xindex = -1

		try:
			yindex = suffixes.index(ysuffix)
		except:
			yindex = -1

		if xindex < yindex:
			return 1
		elif xindex > yindex:
			return -1
		else:
			try:
				xx = float(xsize[:-2])
				yy = float(ysize[:-2])

				if xx < yy:
					return 1
				elif xx > yy:
					return -1
			except:
				pass

		return 0


	def getPartitions(self, host):
		partitions = []

		rows = self.db.execute("""select p.mountpoint, p.partitionsize
			from partitions p, nodes n where p.node = n.id and
			n.name = '%s'""" % (host))

		if rows > 0:
			for (mnt, size) in self.db.fetchall():
				if mnt in [ '', 'swap' ]:
					continue
				if len(mnt) > 0 and mnt[0] != '/':
					continue

				partitions.append((size, mnt))

		return partitions


	def getLargestPartition(self, host):
		#
		# get the mountpoint for the largest partition for a host
		#
		maxmnt = None

		sizelist = self.getPartitions(host)
		if len(sizelist) > 0:
			sizelist.sort(self.partsizeCompare)
			(maxsize, maxmnt) = sizelist[0]

		return maxmnt


	def getPhysHost(self, vm_host):
		#
		# get the physical host that controls this VM host
		#
		host = None

		rows = self.db.execute("""select vn.physnode from vm_nodes vn,
			nodes n where n.name = '%s' and n.id = vn.node"""
			% (vm_host))

		if rows == 1:
			physnodeid, = self.db.fetchone()
			rows = self.db.execute("""select name from nodes where
				id = %s""" % (physnodeid))

			if rows == 1:
				host, = self.db.fetchone()

		return host


	def isVM(self, host):
		#
		# a node is a VM if it is in the vm_nodes table
		#
		try:
			rows = self.db.execute("""select n.name from
				nodes n, vm_nodes vn where
				n.name = '%s' and n.id = vn.node""" % host)
		except:
			rows = 0

		return rows

