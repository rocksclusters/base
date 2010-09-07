#!/opt/rocks/bin/python
#
# The primary agent for 411 clients. A greceptor listener module that
# responds to signed 411-alerts from the master node.
#
# Original Author 2003 Federico Sacerdoti 
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
# $Log: listen411.py,v $
# Revision 1.6  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.3  2008/07/16 22:33:59  bruno
# don't republish 411 alerts.
#
# this causes a traffic storm on large clusters and all other 411 listeners
# will toss the message any way (411 listeners only accept messages from the
# frontend).
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
# Revision 1.10  2007/06/23 04:03:38  mjk
# mars hill copyright
#
# Revision 1.9  2006/09/11 22:48:46  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:10:53  mjk
# 4.2 copyright
#
# Revision 1.7  2006/01/16 23:05:35  bruno
# applied fix from federico sacerdoti
#
# Revision 1.6  2006/01/16 06:49:09  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:09:41  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:18  mjk
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
# Revision 1.29  2005/01/24 23:37:44  fds
# Using my simplehttp library for transfers in 411. No memory leaks, no more
# forking from threads. TCP retries now greatly simplified in the listener.
#
# Revision 1.28  2005/01/04 22:09:02  fds
# Retry multiple times if necessary, dont rely on TCP.
#
# Revision 1.27  2004/11/02 01:39:53  fds
# Converge faster by increasing load on frontend papache server (suggesion by phil).
#
# Revision 1.26  2004/11/02 00:43:26  fds
# Listening to Phil. Put more load on frontend apache's server. Should lead
# to faster 411 convergence on large clusters. Also use correct mcast channel.
#
# Revision 1.25  2004/10/04 19:19:09  fds
# A non-zero DMAX for 411 feedback metrics. Made possible by new
# cluster-gmetric page.
#
# Revision 1.24  2004/09/07 21:50:22  fds
# 80-col, better error handling.
#
# Revision 1.23  2004/07/21 17:46:46  fds
# Alerts handle group names with spaces. Important
# for Rocks Membership names
#
# Revision 1.22  2004/07/21 00:50:25  fds
# 411get listing now respects groups. Moved group processing into
# base class.
#
# Revision 1.21  2004/07/20 19:47:17  fds
# 411 group support. Also cleaned out some depricated options.
#
# Revision 1.20  2004/06/08 21:41:35  fds
# 80-col code and fix error reporting.
#
# Revision 1.19  2004/03/25 03:15:11  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.18  2004/03/09 18:27:11  fds
# Dont graph info metric, type is now timestamp.
#
# Revision 1.17  2004/03/09 02:31:30  fds
# 411 hardcore. Achieve reliable multicast the same way ganglia does:
# repeat yourself until you are hoarse. Use 'receptor' classes to inform
# a Repeater411 metric of new alerts, which are then re-published every
# 20sec for an hour.
#
# Assumes receipt of your own mcast packet is reliable. This design should
# achieve reliable 411 alerts in the long run, while maintaining simplicity.
#
# Revision 1.16  2003/10/30 02:31:33  fds
# Small changes
#
# Revision 1.15  2003/10/20 19:31:38  fds
# Respect to master scores, better doc formatting.
# Turned off debug mode for all modules.
#
# Revision 1.14  2003/09/26 17:33:54  fds
# Cleaner isUs check, not overly Exceptionriffic.
#
# Revision 1.13  2003/09/25 18:18:08  fds
# Ignoring alerts from ourselves.
#
# Revision 1.12  2003/09/09 01:44:42  fds
# Using Master helper class. Started
# structure for complex 411 service.
#
# Revision 1.11  2003/09/08 05:17:53  fds
# On our way to using URLs
#
# Revision 1.10  2003/09/08 05:09:05  fds
# Parsing character data in conf file. Not Used, ugly code, slow.
#
# Revision 1.9  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.8  2003/08/13 21:48:27  fds
# Saved case where child does not exit cleanly on failure.
#
# Revision 1.7  2003/08/09 01:01:31  fds
# Dont do too much in the constructor.
#
# Revision 1.6  2003/07/23 18:47:55  fds
# Added 'disable' option to the config file.
#
# Revision 1.5  2003/07/22 22:19:45  fds
# Getting ready for packaging.
#
# Revision 1.4  2003/07/21 23:46:22  fds
# Listener does not need a configuration file, can incorporate new masters dynamically.
#
# Revision 1.3  2003/07/16 21:28:56  fds
# Sign, verify deal with base64 signatures now, header format improved.
#
# Revision 1.2  2003/07/16 06:19:48  fds
# Moved sign and verify tasks to service411. Allowed for multiple master
# servers in listeners, even dynamically discovered ones (as long as they
# are identified and put into self.masters). Master servers identified by
# IP address.
#
# Revision 1.1  2003/07/15 23:48:57  fds
# New 411 alert design.
#
# Revision 1.1  2003/07/02 23:26:09  fds
# A low frequency 411 pull engine (Ganglia independant).
#
#

import os
import os.path
import sys
import time
import random
import gmon.events
import gmon.gmetric
import gmon.Network
import rocks.service411
import urllib
from rocks.service411 import Error411
from gmon.director import ReceptorError


# Multiple inheritance with a bias towards Listener.
class Listen411(gmon.events.Listener, rocks.service411.Service411):
	"""Detects a changed 411 file, and pulls it from the first available
	master server. Names the file correctly on the local machine."""

	def __init__(self, app):
		rocks.service411.Service411.__init__(self)
		gmon.events.Listener.__init__(self, app)
		# One per master IP
		self.stamps = {}
		# One per 411 file
		self.files = {}
		self.receptor.alerts = {}
		self.tx = gmon.gmetric.Tx()

		# Start out with masters from conf file.
		for master in self.masters:
			self.stamps[master.getAddress()] = 0

		self.groupPaths = []
		for g in self.groups:
			if not g: continue
			self.groupPaths.append('/'.join(g))

		self.debug = 0

		if self.debug:
			print "411 listening for groups", self.groupPaths


	def name(self):
		"""The metric name we're interested in."""

		if self.disable:
			return None
		else:
			return "411alert"


	def isUs(self, address):
		"""Determines if the address is one from one of our interfaces.
		Returns 1 if the address is from us, 0 otherwise."""

		if self.debug:
			return 0

		intfs = gmon.Network.interfaces()

		# In a departure from traditional UNIX programming, we check
		# all our network interfaces :)

		for i in intfs:
			our_ip = intfs[i].split('/')[0]
			if address == our_ip:
				return 1
		return 0


	def addAlert(self, alert, url):
		"""Adds an alert to the warm list in our receptor. Url is the
		verified 411 file url."""

		self.receptor.getLock()

		alert['TN'] = time.time()
		alert['URL'] = url

		# Hash on url ensures we only have the latest alert per file.
		self.receptor.alerts[url] = alert

		self.receptor.releaseLock()


	def isInteresting(self, master):
		"""Returns 1 if the group portion of a master's url matches one
		of our groups. A substring match is used."""

		# No starting or trailing slashes in group.
		path = master.getDir()
		group = path.replace(self.urldir, '')
		group = group[2:-1]

		for g in self.groupPaths:
			if g.find(group) == 0:
				return 1
		return 0


	def run(self, metric):
		"""Checks the message signature, and retrieves the 411
		file if appropriate. Supports multiple master servers, which
		may be dynamically discovered."""

		try:
			msg, sig = metric["VAL"].split("\n", 1)
			url, seqnum_string = msg.split(" ")
			seqnum = float(seqnum_string)

			url = urllib.unquote(url)
			master = rocks.service411.Master(url)
			address = master.getAddress()
		except:
			self.warning("alert not in the correct format")
			return

		if not self.verify(msg, sig):
			# Could be from another cluster, be quiet.
			return

		if address not in self.stamps:
			# This message is possibly from a new master.
			# Master is not spoofed since signature verified.

			if not self.isUs(address):
				# Do not record ourselves as a new master.
				try:
					self.addMaster(master)
					self.config.write()
				except:
					self.warning("config error %s: %s"
						% (sys.exc_type, sys.exc_value))

		if url not in self.files:
			# We have not seen this file from this master yet.
			self.files[url] = 0

		if seqnum <= self.files[url]:
			# We have already seen this alert.
			return

		# Things look OK.
		self.stamps[address] = seqnum

		if self.isUs(address):
			# Put this new alert from us on repeat, then finish.
			self.addAlert(metric, url)
			return

		if not self.isInteresting(master):
			if self.debug:
				print "We are not interested in group", \
					master.getDir()
			return

		N = self.app.clusterSize()
		maxbackoff = N / 100.0

		# Random backoff relative to cluster size. Moderate
		# load on master HTTP server
		time.sleep(random.uniform(0, maxbackoff))
		try:
			contents, meta = self.get(url)
			self.write(contents, meta)

		except Error411, msg:
			self.warning("on alert for %s: %s" % (url, msg))
			# More backoff variance on error
			maxbackoff = N / 8.0

		else:
			# Success
			if self.debug:
				print "Wrote: %s" % meta['Name']

			# If we failed on the GET, retry at the next
			# repeated alert.
			self.files[url] = seqnum


def initEvents():
	return Listen411
