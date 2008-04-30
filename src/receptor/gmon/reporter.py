#!/opt/rocks/bin/python
#
# The Reporter thread for the greceptor daemon. Listens on the Ganglia 
# multicast channel for specific metrics. Allows for immediate event-based
# ganglia triggers.
#
# $Id: reporter.py,v 1.2 2008/03/06 23:41:45 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# $Log: reporter.py,v $
# Revision 1.2  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:44  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.8  2007/06/23 04:03:40  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:48:54  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:10:58  mjk
# 4.2 copyright
#
# Revision 1.5  2006/06/30 12:26:32  bruno
# moved all ganglia python code in hpc roll to point to the rocks foundation
# python
#
# Revision 1.4  2005/10/12 18:09:50  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:03:27  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:22:51  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:50:27  fds
# Greceptor. Moved from monolithic source tree.
#
# Revision 1.6  2004/11/04 00:00:40  fds
# Greceptor needs to listen on the gmond channel too.
#
# Revision 1.5  2004/03/25 03:15:05  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.4  2003/10/30 02:27:31  fds
# Python 2.2.3 does not recognize multiple inheritance with issubclass().
# Very annoying, and now we have to remove a useful test.
#
# Revision 1.3  2003/10/17 23:36:16  fds
# Looking good on mpd failure, resurrecting the ring.
#
# Revision 1.2  2003/10/17 23:04:26  fds
# Closer...
#
# Revision 1.1  2003/10/17 19:24:07  fds
# Presenting the greceptor daemon. Replaces gschedule and glisten.
#
#

import sys
import types
import time
import socket
import struct
import gmon.Gmetric
import gmon.gmetric
from gmon.director import ReceptorThread
from gmon.events import Listener
import thread
		
		
		
class Reporter(ReceptorThread):
	"""Listens to the Ganglia multicast channel for specific
	metrics, and takes appropriate action. Similar to the rocks
	gschedule daemon.
	"""

	def __init__(self, app):
		ReceptorThread.__init__(self)
		self.app = app
		self.port = 8649
		self.tx = gmon.gmetric.Tx()
		self.listeners = {}
		self.cleaningwindow = 60
		self.lastcheck = time.time()
		self.sock = None


	def addListener(self, listenclass):
		"""Determines if the listener is a well formed class, and
		schedules it. Listener can opt-out by providing a null name."""

		if type(listenclass) == types.ClassType:
			listener = listenclass(self.app)
			name = listener.name()
			if name:
				self.listeners[name] = listener


	def run(self):
		"""Listens on Ganglia's multicast channel for interesting metrics"""

		# Listen for both multicast and unicast Ganglia messages
		channel = ("", self.port)

		# Open up a UDP multicast socket, do the Multicast receiver dance.
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
		# Listen to loopback interface too
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
		
		# Join multicast group. Matching 'struct ip_mreq' C structure.
		mreq = struct.pack("4sL", socket.inet_aton(self.tx.getChannel()), 
			socket.INADDR_ANY)
		#print "Multicast membership request is %s" % `mreq`
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, 
			mreq)

		self.sock.bind(channel)

		# Listen on the limited broadcast address 255.255.255.255 
		# (non-routed) as well.

		print "Listening on Ganglia multicast channel", channel
		
		while 1:
			msg, sender = self.sock.recvfrom(1500)
			ip, port = sender
			#print "Got message from %s:%s" % (ip, port)
			now = time.time()

			# Interpret the Ganglia 2.5.x XDR message format.
			try:
				metric = gmon.Gmetric.parse(msg)
			except gmon.Gmetric.error, errmsg:
				self.app.warning(errmsg)
				continue

			# Include the sending host's IP address.
			metric["IP"] = ip

			# Update clustersize estimator.
			self.app.estimator_lock.acquire()
			self.app.hosts[ip] = now
			self.app.estimator_lock.release()

			if self.app.doXML:
				self.showXML(sender, metric)
				#continue

			name = metric["NAME"]
			#print "Metric name %s" % name

			if name in self.listeners:
				# Call the listener with this message. Assumes only one
				# listener per metric name.
				l = self.listeners[name]
				if self.app.doDebug:
					print "Recieved msg for %s" % l.__class__
					self.showXML(sender, metric)
					l.run(metric)
				else:
					try:
						l.run(metric)
					except:
						oops = "%s threw exception '%s %s', removing it." \
							% (l, sys.exc_type, sys.exc_value)
						self.app.warning(oops)
						del(self.listeners[name])



	def showXML(self, sender, metric):
		"""Prints an XML snippet representing this message.
		Does not know Cluster name, etc."""

		host_string = '<HOST IP="%s" REPORTED="%d" TN="0" TMAX="20" ' % \
			(sender[0], int(time.time()))
		host_string += 'DMAX="0" LOCATION="" GMOND_STARTED="-1">'

		metric_string = '<METRIC NAME="%s" VAL="%s" TYPE="%s" UNITS="%s" ' % \
			(metric["NAME"], metric["VAL"], metric["TYPE"], metric["UNITS"])

		metric_string += 'TN="0" TMAX="%s" DMAX="%s" SLOPE="%s" SOURCE="%s"/>' % \
			(metric["TMAX"], metric["DMAX"], metric["SLOPE"], metric["SOURCE"])

		print host_string
		print metric_string
		print "</HOST>"
		print
		sys.stdout.flush()



