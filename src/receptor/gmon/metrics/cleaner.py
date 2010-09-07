#!/opt/rocks/bin/python
# 
# A sample metric event for greceptor.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# $Log: cleaner.py,v $
# Revision 1.5  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.4  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:44  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.10  2007/06/23 04:03:40  mjk
# mars hill copyright
#
# Revision 1.9  2006/09/11 22:48:54  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:10:59  mjk
# 4.2 copyright
#
# Revision 1.7  2006/06/30 12:26:32  bruno
# moved all ganglia python code in hpc roll to point to the rocks foundation
# python
#
# Revision 1.6  2006/01/16 06:49:11  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:50  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:27  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:25:01  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:22:52  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:50:27  fds
# Greceptor. Moved from monolithic source tree.
#
# Revision 1.7  2004/07/21 19:57:48  fds
# Make /var/cluster
#
# Revision 1.6  2004/03/25 03:15:05  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.5  2003/11/17 18:55:24  fds
# Fixes from rockstar testing. Cluster top works again.
#
# Revision 1.4  2003/11/01 01:54:07  fds
# Using jolt mechanism to really keep KAgreement quiet in the common case.
#
# Revision 1.3  2003/10/17 23:36:17  fds
# Looking good on mpd failure, resurrecting the ring.
#
# Revision 1.2  2003/10/17 23:04:26  fds
# Closer...
#
# Revision 1.1  2003/10/17 19:24:08  fds
# Presenting the greceptor daemon. Replaces gschedule and glisten.
#
#

import time
import gmon.events

class Cleaner(gmon.events.Metric):
	"""A metric to prune old hosts from the cluster size estimator, which
	is created by the Reporter thread. We do not send any metrics."""

	def __init__(self, app):
		gmon.events.Metric.__init__(self, app, 90)
		self.window = 80

	def name(self):
		return "host-cleaner"		
		
	def run(self):
		"""We prune a host if they are dead as per the ganglia definition:
		4 * heartbeat interval (80s). Assumes no listener will take longer than
		this to complete."""

		self.app.estimator_lock.acquire()
		now = time.time()

		died = []
		for h, lastmsg in self.app.hosts.items():
			if lastmsg <  now - self.window:
				died.append(h)
				print "Pruning dead host", h

		for h in died:
			del self.app.hosts[h]

		size = len(self.app.hosts)

		self.app.estimator_lock.release()

		# Write the estimate to a file for others to use.
		try:
			f = open('/var/cluster/size-estimate', 'w')
			f.write('%s\n' % size)
			f.close()
		except:
			pass



def initEvents():
	return Cleaner
		
