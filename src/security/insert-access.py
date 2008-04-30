#! /opt/rocks/bin/python
#
# Insert-access for secure WAN kickstart
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
# $Log: insert-access.py,v $
# Revision 1.14  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.13  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.12  2006/09/11 22:47:27  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/27 22:29:43  bruno
# stable (mostly) after integration of new foundation and localization code
#
# Revision 1.9  2006/01/23 21:35:30  yuchan
# update for supporting multi-byte
#
# Revision 1.8  2006/01/16 06:49:01  mjk
# fix python path for source built foundation python
#
# Revision 1.7  2005/12/14 18:57:50  bruno
# make sure you create an 'all' directory when the '--all' flag is thrown
#
# Revision 1.6  2005/10/12 18:08:45  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:02:24  mjk
# updated copyright
#
# Revision 1.4  2005/07/11 23:51:37  mjk
# use rocks version of python
#
# Revision 1.3  2005/05/24 21:21:59  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/03/26 01:41:30  fds
# Handles remove action in lockdown
#
# Revision 1.1  2005/03/26 01:01:56  fds
# New rocks-security package
#
# Revision 1.1  2005/03/01 02:02:41  mjk
# moved from core to base
#
# Revision 1.9  2005/01/06 22:45:52  fds
# Going through the docs for 3.4 in my head. --roll option does not give
# kickstart access, only rpm access.
#
# Revision 1.8  2004/11/02 01:47:08  fds
# Typo
#
# Revision 1.7  2004/11/02 00:40:32  fds
# Can do roll access. No need for roll-access.py anymore.
#
# Revision 1.6  2004/09/07 23:05:54  fds
# Correctly show ip address when using named access
#
# Revision 1.5  2004/07/27 17:59:38  fds
# Uses rocks.security and new sbin/wan location.
#
# Revision 1.4  2004/06/30 23:39:38  fds
# Moving to new sbin structure
#
# Revision 1.2  2004/06/23 17:46:18  fds
# Added lock file, better error handling
#
# Revision 1.1  2004/06/22 23:27:09  fds
# First Design
#
#


import sys
import os
import time
import signal
import curses
import socket
import snack
import rocks.util
import rocks.kickstart
import rocks.security

from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ('insert-access')


class App(rocks.kickstart.Application):
	"""Inserts access for WAN kickstart hosts on a central server.
	Can be used to enable a roll server, so anonymmous users may
	access your rolls."""

	def __init__(self, argv):
		rocks.kickstart.Application.__init__(self, argv)
		self.usage_name = "Insert Access"
		self.usage_version = "@VERSION@"
		self.do_all = 0
		self.screen = None
		self.inserted = []
		self.allow = ''
		self.baseDir = '/var/www/html/install/sbin/wan'
		self.baseUrl = '/install/sbin/wan'
		self.security = rocks.security.Modes(self.baseDir)
		self.rcfileHandler = RCFileHandler
		self.do_verbose = 0
		self.rolls = 0
		self.permanent = 0
		self.remove = 0
		self.debug = None
		self.lockFile = '/var/lock/insert-access'

		self.getopt.s.extend(['v'])
		self.getopt.l.extend([
			('all', 'allow anyone'),
			('rolls', 'access to rolls'),
			('remove', 'revoke access'),
			('stop', 'same as remove'),
			('permanent', 'long-lived access'),
			'verbose'
			])


	def usageTail(self):
		return """Address

Address can be any valid Apache allow directive, including ranges."""


	def parseArg(self, c):
		rocks.kickstart.Application.parseArg(self, c)

		key, val = c
		if key in ("--all",):
			self.do_all = 1
			self.allow = 'all'
			self.rolls = 1
		elif key == "--rolls":
			self.rolls = 1
		elif key == "--permanent":
			self.permanent = 1
		elif key in ("--remove","--stop"):
			self.remove = 1
		elif key in ('-v', '--verbose'):
			self.do_verbose += 1
			self.debug = open('./debug.txt', 'w')
			self.debug.write("%s starting\n" %  self.usage_name)


	def cleanup(self):
		self.security.endPublicMode()
		self.endGUI()
		try:
			os.unlink(self.lockFile)
		except:
			pass


	def startGUI(self):
		self.screen = snack.SnackScreen()

		self.form = snack.GridForm(self.screen,
			_("Clusters from %s") % self.allow, 1, 1)

		self.textbox = snack.Textbox(50, 4, "", scroll=1)
		self.form.add(self.textbox, 0, 0)

		self.screen.drawRootText(0,0,
			_("%s -- version %s") % (self.usage_name, self.usage_version))

		self.screen.pushHelpLine(' ')


	def endGUI(self):
		if self.screen:
			self.screen.finish()


	def statusGUI(self):
		"""Draws all the discovered clients"""
		
		lines=''
		for ip, name, count in self.inserted:
			lines += '%s \t\t %s \t (%s)\n' % (ip, name, count)

		self.textbox.setText(lines)
		self.form.draw()
		self.screen.refresh()


	def printDiscovered(self, ip):
		"""Briefly shows that we found a new client"""

		form = snack.GridForm(self.screen,
			_("Discovered New Cluster"), 1, 1)

		msg = _("Discovered a new cluster at IP %s") % ip
		textbox = snack.Textbox(len(msg), 1, msg)
		form.add(textbox, 0, 0)

		form.draw()
		self.screen.refresh()
		time.sleep(1.5)
		self.screen.popWindow()


	def discover(self, line):
		"""Determines if an access has occured"""

		# We assume standard Apache log format
		if self.do_verbose:
			self.debug.write("Considering %s\n" % line)
			self.debug.flush()

		if not line.count('GET ' + self.baseUrl):
			return 0
		fields = line.split()
		try:
			status = int(fields[8])
		except:
			raise ValueError, _("Apache log file not well formed!")

		if status != 200:
			if self.do_verbose:
				self.debug.write('HTTP status: %s\n' % (status))
				self.debug.flush()
			return 0

		client = fields[0]
		hostname = 'unknown'
		try:
			host = socket.gethostbyaddr(client)
			hostname = host[0]
			ip = host[-1][0]
		except:
			ip = client

		found = 0
		for peer in self.inserted:
			addr, host = peer[:2]
			if addr == ip and host == hostname:
				peer[2] += 1
				found = 1

		if not found:
			peer = [ip, hostname, 1]
			self.inserted.insert( 0, peer )
		self.printDiscovered(ip)
		return 1


	def run(self):

		# Roll access and remove generally operate on all client.
		if (self.remove or self.rolls) and not self.args:
			self.allow = 'all'
		elif self.args:
			self.allow = self.args[0]
		elif not self.do_all:
			self.usage()
			sys.exit(1)
			
		if os.path.isfile(self.lockFile):
			raise Exception, _("lock file %s exists") % self.lockFile

		wanroot = os.path.join(self.dist.getHomePath(), 'wan')
		if self.remove:
			self.security.removeAccess(wanroot, self.allow)
			self.security.endPublicMode()
			print "Removed wan kickstart and roll access to %s" \
				% self.allow
			return

		if self.rolls:
			self.security.insertRollAccess(wanroot, self.allow)
			print "Opened wan roll access to %s" % self.allow
			return

		self.security.startPublicMode(self.allow)

		if self.permanent:
			print "Opened permanent wan kickstart access to %s" \
				% self.allow
			return

		os.system('touch %s' % self.lockFile)

		log = open('/var/log/httpd/ssl_access_log', 'r')
		log.seek(0,2)

		self.startGUI()
		self.screen.pushHelpLine(_(" Press <F10> to quit "))
		self.form.addHotKey('F10')
		self.form.setTimer(1000)

		self.statusGUI()

		result = self.form.run()
		while result == 'TIMER':
			line = log.readline()
			if not line:
				result = self.form.run()
				continue

			if not self.discover(line):
				continue
			
			self.statusGUI()

		log.close()
		if self.do_verbose:
			self.debug.close()
		self.cleanup()



class RCFileHandler(rocks.kickstart.RCFileHandler, rocks.security.RCFileHandler):
    
	def __init__(self, app):
		rocks.kickstart.RCFileHandler.__init__(self, app)
		rocks.security.RCFileHandler.__init__(self, app.security)



# Signal Handler
def Cleaner(signum, frame):

	app = frame.f_locals['self']
	app.cleanup()
	print "Cleaning up..."
	sys.exit(0)

signal.signal(signal.SIGINT, Cleaner)



# My Main
app = App(sys.argv)
app.parseArgs()
try:
	app.run()
except Exception, msg:
	sys.stderr.write("error - %s\n" % msg)
	app.cleanup()
	sys.exit(1)
