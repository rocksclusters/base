# $Id: __init__.py,v 1.12 2012/11/27 00:48:26 phil Exp $
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
#

import os
import string
import rocks.gen
import rocks.commands
import tempfile
	
class Command(rocks.commands.run.command):
	"""
	Generates a script which can be used to reconfigure a system after 
	some attributes have been changed.
	
	<param type='boolean' name='clear'>
	If clear is true the command will remove all the _old attributes.
	This command should be run at the beginning of a reconfigure session.
	Default is 'no'.
	</param>

	<param type='boolean' name='showattr'>
	It only prints the attribute that will be changed when running reconfigure
	Default is 'no'.
	</param>

	<arg optional='1' type='string' name='roll' repeat='1'>
	Not implemented. This argument is not implemented
	</arg>

	<example cmd='run reconfigure'>
	Generate a script to reconfigure the current system
	</example>
	"""

	def run(self, params, args):

		(clear, showattr) = \
			self.fillParams([
				('clear', 'n'),
				('showattr', 'n')
			])

		hostname = 'localhost'
		if self.str2bool(showattr) :
			# TODO implement this
			print "show attr", showattr
			return

		if self.str2bool(clear) :
			# TODO implement this
			return


		script = []
		script.append('#!/bin/sh\n')
			
		rolls = []
		for roll in args:
			rolls.append(roll)
		xml = self.command('list.host.xml', [ 'localhost', 
			'roll=%s' % string.join(rolls, ',') ])


		if self.os != 'linux':
			self.abort('it runs only on linux!!')
		
		gen = rocks.gen.Generator_linux()
		# set reconfigure stage
		gen.set_reconfigure(True)
		gen.parse(xml)
		cur_proc = False
		for line in gen.generate('post'):
			if not line.startswith('%post'):
				script.append(line)
			else:
				if cur_proc == True:
					script.append('__POSTEOF__\n')
					script.append('%s %s\n' % (interpreter, t_name))
					cur_proc = False
				try:
					i = line.split().index('--interpreter')
				except ValueError:
					continue
				interpreter = line.split()[i+1]
				t_name = tempfile.mktemp()
				cur_proc = True
				script.append('cat > %s << "__POSTEOF__"\n' % t_name)
		
		self.addText(string.join(script, ''))


