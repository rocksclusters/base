#!/opt/rocks/bin/python
#
# A greceptor metric to help get out the word on 411alerts. Used
# especially for large clusters.
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
# $Log: repeater411.py,v $
# Revision 1.4  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.1  2007/12/10 21:28:33  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.9  2007/06/23 04:03:38  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:48:48  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:49:10  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:41  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:19  mjk
# updated copyright
#
# Revision 1.3  2005/08/08 21:24:59  mjk
# foundation
#
# Revision 1.2  2005/05/24 21:22:44  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:40  mjk
# moved from core to base
#
# Revision 1.5  2005/01/18 16:39:37  fds
# Use broadcast alert signaling rather than multicast.
#
# Revision 1.4  2004/11/02 00:57:04  fds
# Same channel/port as gmond. For bug 68.
#
# Revision 1.3  2004/07/29 00:25:48  fds
# Combating a strange int overflow error seen on opterons.
#
# Revision 1.2  2004/03/25 03:15:12  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.1  2004/03/09 02:31:30  fds
# 411 hardcore. Achieve reliable multicast the same way ganglia does:
# repeat yourself until you are hoarse. Use 'receptor' classes to inform
# a Repeater411 metric of new alerts, which are then re-published every
# 20sec for an hour.
#
# Assumes receipt of your own mcast packet is reliable. This design should
# achieve reliable 411 alerts in the long run, while maintaining simplicity.
#
#

import time
import gmon.events

class Repeater411(gmon.events.Metric):
	"""Repeats the last 411 alert for every file. Has a function on a 411
	master only."""

	def __init__(self, app):
		gmon.events.Metric.__init__(self, app)
		self.setFrequency(20)
		self.setChannel('255.255.255.255')

		# Repeat alerts for 1hr.
		self.repeatfor = 3600


	def name(self):
		return "411-repeater"

	def getAlarm(self):
		return 15


	def run(self):
		"""Republishes warm 411 alerts."""

		r = self.getReceptor("411alert")
		if not r:
			self.warning("Cannot find a 411alert receptor for Repeater")
			return
			
		r.getLock()

		# A list of metric dicts
		alerts = r.alerts

		# Clean out cold alerts.
		now = time.time()
		for a in r.alerts.values():
			age = now - a['TN']
			if age > self.repeatfor:
				del r.alerts[a['URL']]

		# Re-Publish warm alerts
		for a in r.alerts.values():
			self.publish(a['NAME'], a['VAL'],
				a['UNITS'], a['SLOPE'],
				a['TMAX'], a['TMAX'])

		r.releaseLock()




def initEvents():
	return Repeater411
