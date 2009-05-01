#
# $Id: ConfigPartitions.py,v 1.14 2009/05/01 19:06:48 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: ConfigPartitions.py,v $
# Revision 1.14  2009/05/01 19:06:48  mjk
# chimi con queso
#
# Revision 1.13  2009/02/02 18:32:30  bruno
# fixes for software RAID
#
# Revision 1.12  2009/01/23 23:46:50  mjk
# - continue to kill off the var tag
# - can build xml and kickstart files for compute nodes (might even work)
#
# Revision 1.11  2008/10/18 00:55:44  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:30  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:18  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:46:56  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:24  mjk
# 4.2 copyright
#
# Revision 1.6  2005/10/12 18:08:27  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:02:07  mjk
# updated copyright
#
# Revision 1.4  2005/05/24 21:21:46  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/04/28 21:47:23  bruno
# partitioning function updates in order to support itanium.
#
# itanics need 'parted' as 'sfdisk' only looks at block 0 on a disk and
# itanics put their real partition info in block 1 (this is the GPT partitioning
# scheme)
#
# Revision 1.2  2005/03/12 00:01:50  bruno
# minor checkin
#
# Revision 1.1  2005/03/01 00:22:25  mjk
# moved to base roll
#
# Revision 1.1  2005/02/14 21:55:00  bruno
# support for phil's phartitioning phun
#
#
#

import os
import string
import re
import sys
import syslog
import rocks.sql

#
# uncomment for testing
#
#os.environ['Node_Hostname'] = 'compute-0-1'


class App(rocks.sql.Application):

	def __init__(self):
		rocks.sql.Application.__init__(self)
		self.hostname = None

	def setHostname(self, hostname):
		self.hostname = hostname

	def getPartitionInfo(self):
		partinfo = {}

		self.execute('select partitions.device, partitions.mountpoint, '
			'partitions.sectorstart, partitions.partitionsize, '
			'partitions.partitionid, partitions.fstype, '
			'partitions.partitionflags, partitions.formatflags '
			'from partitions,nodes '
			'where partitions.node = nodes.id and '
			'nodes.name = "%s" ' % self.hostname +
			'order by partitions.device')

		for dev,mnt,sect,size,id,fstype,pflags,fflags in \
								self.fetchall():

			s = (dev,sect,size,id,fstype,pflags,fflags,mnt)

			if dev[0:2] == 'md':
				devbasename = dev
			else:
				a = re.split('[0-9]+$', dev)
				devbasename = a[0]

			if not partinfo.has_key(devbasename):
				partinfo[devbasename] = [ s ]
			else:
				partinfo[devbasename].append(s)

		return partinfo


        def run(self):
		#
		# if we are installing a standalone node (e.g., a frontend
		# or a web server) the database will not be accessible, so
		# don't do anything and just return
		#
		if self.connect():
			partinfo = self.getPartitionInfo()
			print 'dbpartinfo = ', repr(partinfo)
			self.close()
		else:
			print 'dbpartinfo = {}'

		return

