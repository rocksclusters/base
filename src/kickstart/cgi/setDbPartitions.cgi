#!/opt/rocks/bin/python
#
# $Id: setDbPartitions.cgi,v 1.20 2012/11/27 00:48:39 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# $Log: setDbPartitions.cgi,v $
# Revision 1.20  2012/11/27 00:48:39  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.19  2012/09/18 23:33:18  clem
# I need to make kickstart.cgi loadable as a module (I need that in the EC2 roll)
# then i fixed all the other classes in the pylib
#
# Revision 1.18  2012/05/06 05:48:44  phil
# Copyright Storm for Mamba
#
# Revision 1.17  2011/07/23 02:30:47  phil
# Viper Copyright
#
# Revision 1.16  2010/09/07 23:53:07  bruno
# star power for gb
#
# Revision 1.15  2009/05/01 19:07:07  mjk
# chimi con queso
#
# Revision 1.14  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.13  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.12  2007/12/10 21:28:35  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.11  2007/06/23 04:03:23  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:47:17  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:38  mjk
# 4.2 copyright
#
# Revision 1.8  2006/01/16 06:48:59  mjk
# fix python path for source built foundation python
#
# Revision 1.7  2005/10/12 18:08:40  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:02:19  mjk
# updated copyright
#
# Revision 1.5  2005/09/13 19:26:21  bruno
# move to foundation
#
# Revision 1.4  2005/05/24 21:21:55  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/05/23 23:59:24  fds
# Frontend Restore
#
# Revision 1.2  2005/04/28 21:47:24  bruno
# partitioning function updates in order to support itanium.
#
# itanics need 'parted' as 'sfdisk' only looks at block 0 on a disk and
# itanics put their real partition info in block 1 (this is the GPT partitioning
# scheme)
#
# Revision 1.1  2005/03/01 02:02:49  mjk
# moved from core to base
#
# Revision 1.1  2005/02/14 21:53:04  bruno
# added setDbPartitions.cgi for phil's phartitioning phun
#
#
#

import os
import string
import re
import sys
import syslog
import rocks.sql

class App(rocks.sql.Application):

	def __init__(self):
		rocks.sql.Application.__init__(self)
		self.response = ''


	def setPartitionInfo(self, part):
		(dev,sect,size,id,fstype,pflags,fflags,mnt) = part

		rowid = None
		self.execute("""select id from partitions where device='%s'
			and node='%s'""" % (dev, self.nodeid))

		try:
			rowid, = self.fetchone()
		except:
			pass

		if rowid != None:
			#
			# if the partition already exists, update it
			#
			self.execute('update partitions ' + 
				'set mountpoint="%s", ' % mnt + 
				'sectorstart="%s", ' % sect + 
				'partitionsize="%s", ' % size + 
				'partitionid="%s", ' % id + 
				'fstype="%s", ' % fstype + 
				'partitionflags="%s" ' % pflags + 
				'where id="%s" ' % rowid)
		else:
			#
			# this partition info is not in the database,
			# create a new row
			#
			self.execute('insert into partitions ' + 
				'(node, device, mountpoint, ' +
				'sectorstart, partitionsize, ' +
				'partitionid, fstype, ' +
				'partitionflags, formatflags) ' +
				'values (%s, ' % self.nodeid + 
					'"%s", ' % dev + 
					'"%s", ' % mnt + 
					'"%s", ' % sect + 
					'"%s", ' % size + 
					'"%s", ' % id + 
					'"%s", ' % fstype + 
					'"%s", ' % pflags + 
					'"%s");' % fflags)


        def run(self):
		self.connect()

		host = ''
		if os.environ.has_key('REMOTE_ADDR'):
                	host = os.environ['REMOTE_ADDR']

		self.nodeid = self.getNodeId(host)

		if os.environ.has_key('HTTP_X_ROCKS_PARTITIONINFO'):
			partinfo = \
				eval(os.environ['HTTP_X_ROCKS_PARTITIONINFO'])

			for disk in partinfo.keys():
				for part in partinfo[disk]:
					self.setPartitionInfo(part)

		print 'Content-type: application/octet-stream'
		print 'Content-length: %d' % (len(''))
		print ''
		print ''

		self.close()
		return

if __name__ == "__main__":
	app = App()
	app.run()

