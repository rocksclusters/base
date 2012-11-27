#!/opt/rocks/bin/python
#
# The base classes for Event modules used in the ganglia receptor 
# daemon. We do not have a "Trigger" class anymore as it was 
# inherently unscalable.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# $Log: events.py,v $
# Revision 1.9  2012/11/27 00:48:42  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.8  2012/05/06 05:48:48  phil
# Copyright Storm for Mamba
#
# Revision 1.7  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.6  2010/09/07 23:53:08  bruno
# star power for gb
#
# Revision 1.5  2010/08/27 22:58:22  bruno
# for some reason, the PATH variable is not being set in the latest version
# of ganglia
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
# Revision 1.12  2005/01/04 22:09:21  fds
# Better error reporting
#
# Revision 1.11  2004/12/09 01:28:15  fds
# Support for sending gmetrics over broadcast channel. Tested.
#
# Revision 1.10  2004/11/02 00:57:03  fds
# Same channel/port as gmond. For bug 68.
#
# Revision 1.9  2004/03/25 03:15:05  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.8  2003/12/09 01:33:14  fds
# Ensure metrics all get a unique name.
#
# Revision 1.7  2003/11/05 18:45:07  fds
# Watchdogs are back, and stronger than ever. No fancy wait threads needed.
#
# Revision 1.6  2003/11/01 01:54:06  fds
# Using jolt mechanism to really keep KAgreement quiet in the common case.
#
# Revision 1.5  2003/10/22 00:56:42  fds
# Makes Python 2.2.3 happy.
#
# Revision 1.4  2003/10/20 19:29:46  fds
# Jolt method will speed up an events scheduling for one time.
#
# Revision 1.3  2003/10/17 23:04:26  fds
# Closer...
#
# Revision 1.2  2003/10/17 20:02:17  fds
# Cleaning metrics for a brighter smile.
#
# Revision 1.1  2003/10/17 19:24:07  fds
# Presenting the greceptor daemon. Replaces gschedule and glisten.
#
#

import os
import sys
import time
import string
import syslog
import gmon.gmetric
import thread


class Event:
	"""The base class for all receptor modules. Knows
	how to log errors to syslog, and provides some useful
	utilities."""

	def __init__(self):
		pass

	def name(self):
		"""The name of a Ganglia Metric"""
		return self.__class__.__name__

	def run(self):
		pass
		
	def debug(self, msg):
		mesg = "%s debug: %s" % (self.name(), msg)
		syslog.syslog(mesg)
		print mesg

	def info(self,msg):
		mesg = "%s info: %s" % (self.name(), msg)
		syslog.syslog(mesg)
		print mesg

	def warning(self, msg):
		mesg = "%s warning: %s" % (self.name(), msg)
		syslog.syslog(syslog.LOG_WARNING, mesg)
		print mesg

	def which(self, filename, path = None):
		"""Given a search path, find a file. Should be standard in
		python."""
		found = 0

		if not path:
			try:
				path = os.environ['PATH']
			except:
				path = ''

		paths = string.split(path, os.pathsep)
		for p in paths:
			if os.path.exists(os.path.join(p, filename)):
				found = 1
				break
		if found:
			return os.path.abspath(os.path.join(p, filename))
		else:
			return None



class Metric(Event):
	"""A metric publishing event. Called periodically by the Director
	thread, and knows how to burp out a Ganglia multicast packet."""

	def __init__(self, app, frequency=60):
		self.frequency = frequency
		self.app = app
		self.jolted = 0
		self.damaged = 0
		self.tx = gmon.gmetric.Tx()

		
	def getFrequency(self):
		if self.jolted:
			self.jolted = 0
			return 1
		else:
			return self.frequency

	def setFrequency(self, val):
		self.frequency = val
		
	def setChannel(self, c):
		self.tx.setChannel(c)
	
	def setPort(self, p):
		self.tx.setPort(p)

	def jolt(self):
		"""Bumps up scheduling frequency for one time.  We are not
		going to lock the jolted variable, even though it can be
		written by multiple threads. Its state will self-stabalize."""
		self.jolted = 1

	def getAlarm(self):
		"""Catches runaway metrics. No module should take longer 
		than 10 sec, unless specified."""
		return 10

	def setDamaged(self, val):
		"""Called when a watchdog had to interrupt this metric because
		it was taking too long."""
		self.damaged = val

	def isDamaged(self):
		return self.damaged

	def schedule(self, director, now=0):
		director.schedule(self, now)

	def value(self):
		return None

	def units(self):
		return ""
		
	def channel(self):
		return ""

	def slope(self):
		"""The numerical behavior of metric. Is it a counter, gauge,
		etc. Options are positive | negative | both | zero."""
		return "both"

	def tmax(self):
		"The max interval between publishing of this metric"
		# Hard to say a max with the probability, but this is likely.
		return self.getFrequency() * 2

	def dmax(self):
		"""The metric's max age, after which we delete it. Zero
		means the metric is immortal. The default is non-zero
		to be nice to listeners memory requirements."""
		return self.getFrequency() * 10

		
	def publish(self, name, value, units="", slope="", tmax="",
			dmax="", type="", channel=""):
		"""Wrapper for the gmetric.publish() function. Type is
		[int32|uint32|timestamp|double| float]. Channel can be any
		multicast or unicast address."""

		if not units:
			units=self.units()
		if not slope:
			slope=self.slope()
		if not tmax:
			tmax=self.tmax()
		if not dmax:
			dmax=self.dmax()
		if not channel:
			channel=self.channel()

		self.tx.publish(name, value, units, slope, tmax,
			dmax, type=type, channel=channel)


	def run(self):
		"""Publishes a Ganglia metric."""

		name = self.name()
		value = self.value()

		# Give metric a chance to abort.
		if None in (name, value):
			return None

		self.publish(name, value)
			
			
	def getReceptor(self, name):

		if not self.app:
			return
		
		if name in self.app.ganglia:
			return self.app.ganglia[name]
			



class Listener(Event):
	"""Base class for Listeners used by the Reporter thread of receptor.
	These listeners respond to raw Ganglia multicast messages."""

	def __init__(self, app):
		Event.__init__(self)
		# A reference to the receptor daemon.
		# Used to get cluster size estimators, etc.
		self.app = app
		
		# Allocate ourselves a receptor object. If we do it here
		# I'm less worried about a metric accessing it while we are
		# in the middle of creating it.
		self.receptor = Receptor()

		self.app.ganglia[self.name()] = self.receptor


	def run(self, metric):
		pass

	def getReceptor(self):
		return self.receptor
		



class Receptor:
	"""Holds metrics and a mutex lock for a listener module.
	Receptor objects reside in the shared ganglia dictionary,
	and are used to communicate between the Reporter and Director
	threads.

	A thread can only alter a receptor if it has obtained a lock
	for it."""
	
	def __init__(self):
		self.lock = thread.allocate_lock()
		self.metrics = {}

		
	def getLock(self):
		"""A blocking call that waits for the lock."""
		self.lock.acquire()
		
	def releaseLock(self):
		self.lock.release()

	def isLocked(self):
		return self.lock.locked()
		
	def checkLock(self):
		if not self.isLocked():
			raise ReceptorError, "Reading an unlocked receptor!"

	def addMetric(self, metric):
		"""Add a metric to this receptor. Expects a metric dictionary
		as returned by Gmetric.parse().  All cleaning is done relative
		to the time this method is called."""

		self.checkLock()

		# We use the TN attribute to record arrival time.
		metric["TN"] = time.time()

		# We hash metrics by IP since some protocols need to search
		# fast through this list for a specific host.
		ip = metric["IP"]
		self.metrics[ip] = metric


	def getMetrics(self):
		"""Returns the list of metrics. These are the actual
		metrics, be careful modifying them!"""

		self.checkLock()

		return self.metrics


	def clean(self):
		"""Cleans out old metrics from our list"""

		self.checkLock()
		
		now = time.time()
		for m in self.metrics.values():
			age = now - m['TN']
			if m['DMAX'] and age > m['DMAX']:
				del self.metrics[m['IP']]
				# Nice that we have the dict key in our metric.


