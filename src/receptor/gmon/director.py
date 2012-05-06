#!/opt/rocks/bin/python
#
# Director thread of the Greceptor daemon. Schedules metric events
# for publication. Uses ideas from gschedule.
#
# $Id: director.py,v 1.7 2012/05/06 05:48:48 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# $Log: director.py,v $
# Revision 1.7  2012/05/06 05:48:48  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/07/23 02:30:49  phil
# Viper Copyright
#
# Revision 1.5  2010/09/07 23:53:08  bruno
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
# Revision 1.9  2007/06/23 04:03:40  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:48:54  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:58  mjk
# 4.2 copyright
#
# Revision 1.6  2006/06/30 12:26:32  bruno
# moved all ganglia python code in hpc roll to point to the rocks foundation
# python
#
# Revision 1.5  2006/06/27 22:37:47  bruno
# inserted federico sacerdoti's scalability fixes to ganglia
#
# Revision 1.2  2005/05/24 21:22:51  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:50:27  fds
# Greceptor. Moved from monolithic source tree.
#
# Revision 1.6  2004/03/25 03:15:05  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.5  2003/11/05 18:45:07  fds
# Watchdogs are back, and stronger than ever. No fancy wait threads needed.
#
# Revision 1.4  2003/11/01 01:54:06  fds
# Using jolt mechanism to really keep KAgreement quiet in the common case.
#
# Revision 1.3  2003/10/30 02:27:31  fds
# Python 2.2.3 does not recognize multiple inheritance with issubclass().
# Very annoying, and now we have to remove a useful test.
#
# Revision 1.2  2003/10/20 19:29:46  fds
# Jolt method will speed up an events scheduling for one time.
#
# Revision 1.1  2003/10/17 19:24:07  fds
# Presenting the greceptor daemon. Replaces gschedule and glisten.
#
#


import os
import sys
import types
import string
import random
import signal
import time
import thread
from gmon.events import Metric


class ReceptorError(Exception):
	pass
	
class EventTimeout(Exception):
	pass

class ReceptorThread:

	def __init__(self):
		self.lock = thread.allocate_lock()
		
	def getLock(self):
		return self.lock
		
	def finish(self):
		"""Signals the end of this thread."""
		self.lock.release()
		

				
class Director(ReceptorThread):
	"""Directs the metric-publishing action. Will callback metric
	modules at a regular-random interval they specify. Can read
	the shared (and lock-protected) ganglia metric memory area 
	populated by the Reporter thread."""

	def __init__(self, app, seconds=1):
		ReceptorThread.__init__(self)
		self.app = app
		self.granularity = seconds
		self.events = {}
		self.current_event = None


	def addMetric(self, metric_class):
		"""Determines if a metric is a well formed class, and
		schedules it."""

		if type(metric_class) == types.ClassType:
			event = metric_class(self.app)
			event.schedule(self)
				
	
	def schedule(self, event, now=0):
		"""Called if metric wishes to register. Metrics must have
		a unique name."""
		self.events[event.name()] = event
		if now:
			event.jolt()
			
			
	def deschedule(self, event):
		"""If called, the event will never run again."""
		del self.events[event.name()]


	def runEvent(self, e):
		"""Runs the event with a watchdog timer. Catches exceptions
		coming from the event."""

		if self.app.doDebug:
			print "Running %s" % e.__class__
			e.run()
		else:
			try:
				# Setup watchdog timer. Ok for a thread
				# to call this.
				signal.alarm(e.getAlarm())
				e.run()
			finally:
				# Cancel alarm.
				signal.alarm(0)
		

	def getMetric(self, name):
		"""Returns a named metric object. Dont use this unless you
		know what you are doing, as it can lead to race-conditions
		and memory-leaks."""
		if name in self.events:
			return self.events[name]
		else:
			raise ReceptorError, "Could not find metric %s" \
				% name	
				
				
	def run(self):
		"""Calls each metric event once every F seconds
		on average, with a uniformly-distributed random 
		chance. """
		
		while 1:
			v = random.random() # (0,1], uniform distribution.
			for e in self.events.values():
				frequency = e.getFrequency()
				if not frequency:
					continue
				p = float(self.granularity) / frequency
				if v > p:
					continue
				self.current_event = e.name()
				try:
					self.runEvent(e)
				except EventTimeout:
					self.app.warning(
					 "Watchdog caught %s after %s seconds"
					 % (e.name(), e.getAlarm()),
					 showtraceback=False)
					e.setDamaged(1)
				except:
					self.app.warning(
					 "%s threw exception, removing it." % (e))
					self.deschedule(e)

			time.sleep(self.granularity)
			


