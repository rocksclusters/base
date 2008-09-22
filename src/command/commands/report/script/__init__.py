#
# $Id: __init__.py,v 1.2 2008/09/22 20:20:42 bruno Exp $
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
# $Log: __init__.py,v $
# Revision 1.2  2008/09/22 20:20:42  bruno
# change 'rocks config host interface|network' to
# change 'rocks report host interface|network'
#
# Revision 1.1  2008/07/23 00:01:06  bruno
# tweaks
#
#
#

import sys
import tempfile
import os.path
import rocks.commands
import rocks.gen

class Command(rocks.commands.report.command):
	"""
	Take STDIN XML input and create a shell script that can be executed
	on a host.

	<example cmd='report host interface compute-0-0 | rocks report script'>
	Take the network interface XML output from 'rocks report host interface'
	and create a shell script.
	</example>
	"""

	def scrub(self, xml):
		filename = tempfile.mktemp()

		file = open(filename, 'w')
		file.write(xml)
		file.close()

		scrubed = ''
		cmd = 'xmllint --nocdata %s' % (filename)
		for line in os.popen(cmd).readlines():
			scrubed += line
		
		os.remove(filename)

		return scrubed
		

	def runXML(self, xml):
		list = []

		self.generator.parse(xml)
		list += self.generator.generate('post')
			
		for line in list:
			if line[0:5] == '%post':
				continue

			self.addOutput('', line.rstrip())


	def run(self, params, args):
		self.os, self.arch = self.fillParams([
			('os', self.os),
			('arch', self.arch)
			])

		c_gen = getattr(rocks.gen,'Generator_%s' % self.os)
		self.generator = c_gen()
		self.generator.setArch(self.arch)
		self.generator.setOS(self.os)
		self.generator.setRCSComment('rocks report script')

		self.beginOutput()

		xml = '<?xml version="1.0" standalone="no"?>\n'
		xml += '<kickstart>\n'
		xml += '<post>\n'

		for line in sys.stdin.readlines():
			xml += line

		xml += '</post>\n'
		xml += '</kickstart>\n'

		self.runXML(self.scrub(xml))

		self.endOutput(padChar='')

