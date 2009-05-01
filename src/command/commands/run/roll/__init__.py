# $Id: __init__.py,v 1.2 2009/05/01 19:07:02 mjk Exp $
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
# $Log: __init__.py,v $
# Revision 1.2  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.1  2009/03/06 22:34:16  mjk
# - added roll argument to list.host.xml and list.node.xml
# - kroll is dead, added run.roll
#

import os
import string
import popen2
import rocks.gen
import rocks.file
import rocks.commands
from xml.dom.ext.reader import Sax2

	
class Command(rocks.commands.run.command):
	"""
	Installs a Roll on the fly
	
	<arg optional='1' type='string' name='roll' repeat='1'>
	List of rolls. This should be the roll base name (e.g., base, hpc,
	kernel).
	</arg>

	<example cmd='run roll viz'>		
	Installs the Viz Roll onto the current system.
	</example>
	"""

	def run(self, params, args):

		(dryrun, ) = self.fillParams([('dryrun', )])
		
		if dryrun:
			dryrun = self.str2bool(dryrun)
		else:
			dryrun = True
		
		script = []
		script.append('#!/bin/sh')
			
		rolls = []
		for roll in args:
			rolls.append(roll)
		xml = self.command('list.host.xml', [ 'localhost', 
			'roll=%s' % string.join(rolls, ',') ])


		reader = Sax2.Reader()
		gen = getattr(rocks.gen,'Generator_%s' % self.os)()
		gen.parse(xml)

		distPath = os.path.join(self.command('report.distro')[:-1],
			'rocks-dist')
                tree = rocks.file.Tree(distPath)
                dict = {}
		for file in tree.getFiles(os.path.join(self.arch, 
			'RedHat', 'RPMS')):
			if isinstance(file, rocks.file.RPMFile):
				dict[file.getBaseName()] = file.getFullName()
			
		rpms = []
		for line in gen.generate('packages'):
			if line.find('%package') == -1:
				rpms.append(line)			
		for rpm in rpms:
			if rpm in dict:
				script.append('rpm -Uhv --force --nodeps %s' %
					dict[rpm])


		for line in gen.generate('post'):
			if line.find('%post') == -1:
				script.append(line)
		
		if dryrun:
			self.addText(string.join(script, '\n'))
		else:
			os.system(string.join(script, '\n'))

