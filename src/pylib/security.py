#! /opt/rocks/bin/python
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
# $Log: security.py,v $
# Revision 1.15  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.14  2007/06/23 04:03:24  mjk
# mars hill copyright
#
# Revision 1.13  2006/09/15 02:38:20  mjk
# removed ROCK_ROOT variable, #80 (trac.rocksclusters.org)
#
# Revision 1.12  2006/09/11 22:47:23  mjk
# monkey face copyright
#
# Revision 1.11  2006/08/10 00:09:41  mjk
# 4.2 copyright
#
# Revision 1.10  2006/01/16 06:49:00  mjk
# fix python path for source built foundation python
#
# Revision 1.9  2005/10/12 18:08:42  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/09/16 01:02:21  mjk
# updated copyright
#
# Revision 1.7  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.6  2005/05/27 21:00:20  fds
# insert-access edge case
#
# Revision 1.5  2005/05/24 21:21:57  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/03/30 22:39:57  fds
# Default security level is more normal
#
# Revision 1.3  2005/03/26 01:37:57  fds
# Safer lockdown, in the case we move from a lower security level.
#
# Revision 1.2  2005/03/26 01:06:02  fds
# Added lockdown level and XML rcfile parser.
#
# Revision 1.1  2005/03/01 00:22:08  mjk
# moved to base roll
#
# Revision 1.6  2004/11/02 00:42:04  fds
# Support for roll-access (from roll-access.py)
#
# Revision 1.5  2004/10/15 00:19:18  fds
# Default to max security level for insert-access. Insert-ethers lowers it.
#
# Revision 1.4  2004/10/06 18:31:30  fds
# Security levels
#
# Revision 1.3  2004/08/24 22:11:23  bruno
# if a 'public' file already exists, nuke it before creating a symlink.
#
# Revision 1.2  2004/07/27 18:33:43  fds
# Accessors.
#
#

import os

class Modes:
	"""A class to switch the public/private mode of a frontend. In private
	mode, a client must have a valid SSL certificate (x509) to retrieve a
	kickstart file. In public mode, authentication for kickstart access is
	IP based. See securityrc.xml for full level descriptions."""

	def __init__(self, baseDir="/var/www/html", level=5.0):
		self.baseDir = baseDir
		self.level = level

	def getBase(self):
		return self.baseDir

	def setBase(self, base):
		self.baseDir = base

	def getLevel(self):
		return self.level

	def setLevel(self, val):
		if val < 0:
			val = 0.0
		elif val > 10:
			val = 10.0
		self.level = val
		
	def isLow(self):
		"Returns true if our security level is low, false otherwise"
		
		if self.level <= 5:
			#print "Security Low"
			return 1
		else:
			return 0
			
	def isHigh(self):
		if self.level > 5 and self.level < 9:
			#print "Security High"
			return 1
		else:
			return 0
	
	def isLockdown(self):
		if self.level >= 9:
			#print "Security Lockdown"
			return 1
		else:
			return 0
		

	def makePublic(self):
		"""Creates the 'public' directory. Returns path."""

		os.chdir(self.baseDir)
		if os.path.exists('public'):
			os.unlink('public')
		os.symlink('.', 'public')
		return os.path.join(self.baseDir, 'public')
		
		
	def makePrivate(self):
		"Returns this server to safest state"
		try:
			os.chdir(self.baseDir)
			os.unlink('public')
			os.unlink('.htaccess')
		except:
			pass		


	def startPublicMode(self, allow):
		"""Begins the open-access mode on this server"""

		if self.isLockdown():
			self.makePrivate()
			raise Exception, "We are in Lockdown, no public access"
			
		try:
			self.makePublic()
			access = open('.htaccess', 'w')
		except:
			raise Exception, "cannot write to %s\n" % self.baseDir
		access.write('Allow from %s\n' % allow)
		access.write('Deny from all\n')
		access.close()


	def endPublicMode(self):
		"""Ends the open-access mode on this server.  If security level
		is low we keep default access for nodes in the database.
		This is less secure and vulnerable to an IP spoofing attack,
		but keeps the familiar rocks semantics."""

		if self.isHigh():
			self.makePrivate()
				
		elif self.isLow():
			try:
				path = self.makePublic()
				cmd = ('/opt/rocks/bin/dbreport access > '
					'%s/.htaccess 2> /dev/null' % path)
				os.system(cmd)
			except:
				pass
				
		elif self.isLockdown():
			self.makePrivate()
			
			
	def insertRollAccess(self, wanroot, host):
		"""Gives roll access to this WAN client. Independant
		of security level."""

		os.chdir(wanroot)
		try:
			os.mkdir(host)
		except:
			# This is to prevent collisions between multiple
			# processes.
			if os.path.exists(os.path.join(host,'rolls')):
				return

		# Ensure that kcgi can still add links for this host
		# if necessary

		os.system('chmod 1775 %s' % host)
		os.system('chgrp apache %s' % host)

		os.chdir(host)
		try:
			os.symlink('../rolls', 'rolls')
		except:
			pass
		access=open('.htaccess','w')
		access.write('Allow from %s\n' % host)
		access.write('Deny from all\n')
		access.close()

	
	def removeAccess(self, wanroot, host):
		"""Revokes the host's http access to OS and rolls."""

		if host == "rolls":
			return
		os.chdir(wanroot)
		if os.path.exists(host):
			os.system('rm -rf %s' % host)



class RCFileHandler:
	"""Registers the global security level. Must be inherited
	along with another RCFileHandler class."""
	
	def __init__(self, security):
		"Arg is a rocks.security.Modes object"
		self.security = security

	def startElement_securitylevel(self, name, attrs):
		self.text = ''
		
	def endElement_securitylevel(self, name):
		level = float(self.text)
		self.security.setLevel(level)

