#!/opt/rocks/bin/python
#
# A daemon to coordinate Ganglia metrics and listeners in a 
# scalable manner. This service will be more efficient in memory
# and processing requirements than the gschedule/glisten daemons
# it replaces.
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
# $Log: greceptor.py,v $
# Revision 1.4  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.3  2008/07/31 20:19:34  bruno
# really daemonize greceptor
#
# Revision 1.2  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:44  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.11  2007/06/23 04:03:39  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:48:53  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:10:58  mjk
# 4.2 copyright
#
# Revision 1.8  2006/06/30 12:26:32  bruno
# moved all ganglia python code in hpc roll to point to the rocks foundation
# python
#
# Revision 1.7  2006/06/27 22:37:46  bruno
# inserted federico sacerdoti's scalability fixes to ganglia
#
# Revision 1.2  2005/05/24 21:22:51  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:50:26  fds
# Greceptor. Moved from monolithic source tree.
#
# Revision 1.8  2004/07/27 22:51:22  fds
# Typo
#
# Revision 1.7  2004/06/04 23:19:41  fds
# Min cluster size is 1. May fix mpd not running on frontend.
#
# Revision 1.6  2004/03/25 03:15:04  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.5  2003/11/05 18:45:07  fds
# Watchdogs are back, and stronger than ever. No fancy wait threads needed.
#
# Revision 1.4  2003/10/20 19:30:08  fds
# Small changes.
#
# Revision 1.3  2003/10/17 23:36:16  fds
# Looking good on mpd failure, resurrecting the ring.
#
# Revision 1.2  2003/10/17 23:04:25  fds
# Closer...
#
# Revision 1.1  2003/10/17 19:41:50  fds
# Presenting the greceptor daemon. Replaces gschedule and glisten.
#
#

import os
import sys
import rocks.app
import signal
import syslog
import types
import thread
import inspect
import traceback
from gmon.reporter import Reporter
from gmon.director import Director, ReceptorError, EventTimeout

import pdb

# ReceptorError is in Director class so it can be imported.

class App(rocks.app.Application):
	"""The greceptor daemon for support for multicast-based cluster
	services like KAgreement. Listens on the Ganglia multicast
	channel for interesting metrics, and calls metric gatherers at
	specified intervals.
	
	Ganglia are bundles of nerve cell bodies in the peripheral nervous
	system. Each nerve cell has axons to propagate nerve impulses 
	and dendrites to receive them. The dendrites have receptors to collect
	neurotransmitters released by axons. Ganglia is derived from the
	greek word for knot."""
	
	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)
		self.usage_name = 'Ganglia Receptor Daemon'
		self.usage_version = '@VERSION@'
		self.getopt.l.extend([
			('debug', 'stay in foreground'),
			('xml', 'show ganglia wire msgs in XML')
			])
		self.ganglia = {}
		# Our cluster size estimator, updated by reporter.
		self.hosts = {}
		self.estimator_lock = thread.allocate_lock()
		self.doXML = 0
		self.doDebug = 0

		
	def parseArg(self, c):
		# The correct way to do parseArg(): Look for our own
		# options first. 
		if c[0] == '--debug':
			self.doDebug = 1
		elif c[0] == '--xml':
			self.doXML = 1
		else:
			rocks.app.Application.parseArg(self, c)
			
			
	def stayForeground(self):
		"""Returns false if we should daemonize."""
		return self.doDebug or self.doXML
	
		
	def run(self):
		"""Starts the daemon. Will run until signalled. Using
		the low-level thread module is more honest: we can see
		the issues involved. It also does not hide as much behavior
		as the threading module."""

		self.reporter_thread = Reporter(self)
		self.director = Director(self, seconds=15)
		
		# Load listeners first so receptors get made before use.
		self.loadModules("gmon.listeners", self.reporter_thread.addListener)
		self.loadModules("gmon.metrics", self.director.addMetric)
		
		thread.start_new_thread(self.reporter_thread.run, ())
		
		# We run the director from the main thread so we can set
		# and catch signals for our watchdog.
		while 1:
			try:
				self.director.run()
				signal.pause()
			except EventTimeout:
				# Sometimes the watchdog interrupts here
				msg="Watchdog fired unexpectedly while running "
				msg+="'%s'! " % self.director.current_event
				msg+="Re-running director..."
				self.warning(msg, showtraceback=False)
		

	def fullImport(self, name):
		"""Imports all components of a module, from the
		Python language reference."""

		mod = __import__(name)
		components = name.split('.')
		for comp in components[1:]:
			mod = getattr(mod, comp)
		return mod

		
	def loadModules(self, path, addfunc):
		"""Import all the python code in a directory. Path is 
		like gmon.metrics"""

		info = "greceptor loading %s: " % path
		
		modules = self.fullImport(path)
		for file in os.listdir(modules.__path__[0]):
			modname, ext = os.path.splitext(file)
			if ext == '.py' and modname != '__init__':
				info = info + modname + " "

				fullmodname = "%s.%s" % (path, modname)
				#print "Importing:", fullmodname
				mod = self.fullImport(fullmodname)

				try:
					initEvents = getattr(mod, "initEvents")
				except AttributeError:
					info = info + "(no initEvents(), skipping) "
					continue

				# Call the entry point to get a tuple of event
				# classes.
				events = initEvents()

				if type(events) == types.TupleType:
					for event in events:
						addfunc(event)
				else:
					# There is only one event in this module.
					addfunc(events)

		syslog.syslog(info)
		print info

		
	def info(self, msg):
		syslog.syslog(syslog.LOG_INFO, msg)
		print " greceptor info:", msg

		
	def warning(self, msg, showtraceback=True):
		"""Logs a warning to syslog. Usually after an exception
		was thrown."""

		lines=[]
		lines.append('greceptor: ' + msg)
		if showtraceback:
			lines.append("------greceptor last traceback----")
			lines.extend(apply(traceback.format_exception,
				sys.exc_info()))
			lines.append("------greceptor end traceback-----")
		for line in lines:
			syslog.syslog(syslog.LOG_WARNING, line)
		
		print " greceptor warning:", "\n".join(lines)


	def clusterSize(self):
		"""Returns the value of our cluster size estimator. This value
		is approximately the number of alive hosts. We need this
		figure for modules from both threads."""

		self.estimator_lock.acquire()
		size = len(self.hosts)
		self.estimator_lock.release()

		if (size<1): 
			size = 1

		return size


		
# Setup a signal handler to close the socket when we exit.
# (To save us the socket timeout).

def Cleaner(signum, frame):
	print "Cleaning up..."
	
	# Close the multicast listening socket, so we dont 
	# have to wait a MSL timeout before opening it again. 

	#print frame.f_locals
	reporter_sock = frame.f_locals['self'].app.reporter_thread.sock
	reporter_sock.close()
	
	sys.exit(0)
		

def Watchdog(signum, frame):
	"""Catches hung metrics for the Director."""
	raise EventTimeout
		

signal.signal(signal.SIGINT, Cleaner)
signal.signal(signal.SIGALRM, Watchdog)


# My Main
app=App(sys.argv)
app.parseArgs()

if app.stayForeground():
	app.run()
	
#
# The python Daemon dance. From Steven's "Advanced Programming in the UNIX env".
#
pid = os.fork()
if pid > 0:
	sys.exit(0)

#
# now decouple from parent environment
#
os.chdir("/")# So we can remove/unmount the dir the daemon started in.
os.setsid()  # Create a new session and set the process group.
os.umask(0)

#
# do a second fork
#
pid = os.fork()
if pid > 0:
	#
	# exit from second parent
	#
	sys.exit(0)

# redirect standard file descriptors
sys.stdout.flush()
sys.stderr.flush()
si = file('/dev/null', 'r')
so = file('/dev/null', 'a+')
se = file('/dev/null', 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())

# Start our daemon.
try:
	app.run()
except:
	oops = "daemon threw exception '%s %s'" % (sys.exc_type, sys.exc_value)
	app.warning(oops)

