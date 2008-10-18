#!/opt/rocks/bin/python
#
# Retrives a file using HTTPS for the 411 service. Assumes
# the master servers are running Apache with mod_ssl.
# 
# $Id: 411get.py,v 1.5 2008/10/18 00:55:47 mjk Exp $
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
# $Log: 411get.py,v $
# Revision 1.5  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.4  2008/08/07 20:48:44  anoop
# Add ID and logging info
#

import os
import sys
import string
import rocks.app
from rocks.service411 import Error411

# Multiple inheritance with a bias towards rocks.Application.
class App(rocks.app.Application, rocks.service411.Service411):
	"Can retrieve a 411 file from a set of master servers."

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)
		rocks.service411.Service411.__init__(self)
		self.usage_name = "411 File Retriever"
		self.usage_version = '@VERSION@'
		self.getall = 0
		self.doFile = 0

		self.getopt.s.extend([
			('c:', 'config file'), 'v'
			])

		self.getopt.l.extend([
			('conf=', 'config file'),
			('all', 'retrieve and write all files'),
			('master=', 'master server (url)'),
			('shared=', '411 shared key file'),
			('pub=', 'Master RSA public key file'),
			('comment=', 'file comment character'),
			('local', 'decrypt local 411 msg file'),
			'file',
			('verbose')
			])


	def usageTail(self):
		return """ [filename]
If no filename is given, a list of 411 files is returned."""


	def parseArg(self, c):
		"""Set 411 parameters. If you specify masters and a conf
		file, the masters list argument takes precedence."""

		rocks.app.Application.parseArg(self, c)

		if c[0] in ('--conf', '-c'):
			self.config.setFile(c[1])
			self.config.parse()
		elif c[0] in ('--master',):
			self.masters = [rocks.service411.Master(c[1])]
		elif c[0] in ('--shared',):
			self.shared_filename = c[1]
		elif c[0] in ('--pub',):
			self.pub_filename = c[1]
		elif c[0] == "--comment":
			self.comment = c[1]
		elif c[0] == "--all":
			self.getall = 1
		elif c[0] in ("--local", "--file"):
			self.doFile = 1
		elif c[0] in ("-v", "--verbose"):
			self.verbose += 1

			
	def run(self):
		"""Pull a list of all 411 files, the contents of
		a single one, or write all available files."""

		file = ""
		if self.args:
			file = self.args[0]

		try:
			if file:
				if self.doFile:
					cyphertxt = open(file,'r').read()
					contents, meta = self.decrypt(cyphertxt)
				else:
					contents, meta = self.get(file)
				print contents
				print "### METADATA ###"
				print 'Name: %s\tMode:%s\tOwner=%s' % \
				(meta['name'], meta['mode'], meta['owner'])
			else:
				files = self.find()
				for file in files.keys():
					if not self.getall:
						print file
						continue
					contents, meta = self.get(file)
					self.write(contents, meta, files[file])
					print "Wrote:", meta['name']

		except ValueError:
			raise
			# Thrown by connect() called by get().
			sys.stderr.write("Error: I have no master servers, "
				"check %s.\n" % (self.config.getFile()))
			sys.exit(-1)

		except Error411, msg:
			sys.stderr.write("Error: %s\n" % msg)
			sys.exit(-1)


#
# My Main
#
app = App(sys.argv)
app.parseArgs('four11get')
app.run()
