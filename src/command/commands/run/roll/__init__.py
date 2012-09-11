# $Id: __init__.py,v 1.11 2012/09/11 17:53:40 clem Exp $
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
# $Log: __init__.py,v $
# Revision 1.11  2012/09/11 17:53:40  clem
# Fix for extra newline at the beginning of the generated script
#
# - when using python or other interpreter the extra new line at the beginning
#   of the script move the shebang to the second line and the interpreter
#   was not picked up properly
#
# Revision 1.10  2012/05/06 05:48:33  phil
# Copyright Storm for Mamba
#
# Revision 1.9  2012/02/15 20:09:00  clem
# removed useless popen2
#
# Revision 1.8  2011/08/09 01:03:16  anoop
# If yum install fails due to dependency error,
# force install using rpm --nodeps
#
# Revision 1.7  2011/07/23 02:30:37  phil
# Viper Copyright
#
# Revision 1.6  2011/07/15 23:48:00  anoop
# Rocks run roll needs to honour the "--interpreter" flag
# to the post sections
#
# Revision 1.5  2011/07/13 18:36:29  anoop
# Honour .<arch> directive to yum install.
# When installing packages use,
# "yum install <package>" instead of "yum install <packagefile>.rpm"
#
# Revision 1.4  2011/01/24 22:47:34  mjk
# Use YUM instead of RPM for rocks run roll
# This fixes two issues
# 1) On 64bit we were not installing the 32bit RPMs
# 2) name.arch packages were not being installed
#
# Revision 1.3  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.2  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.1  2009/03/06 22:34:16  mjk
# - added roll argument to list.host.xml and list.node.xml
# - kroll is dead, added run.roll
#

import os
import string
import rocks.gen
import rocks.file
import rocks.commands
import tempfile
from xml.dom.ext.reader import Sax2

rpm_force_template = """[ $? -ne 0 ] && \\
echo "# YUM failed - trying with RPM" && \\
rpm -Uvh --force --nodeps %s\n\n"""
	
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
		script.append('#!/bin/sh\n')
			
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
		rpm_list = {}
		for file in tree.getFiles(os.path.join(self.arch, 
			'RedHat', 'RPMS')):
			if isinstance(file, rocks.file.RPMFile):
				rpm_list[file.getBaseName()] = file.getFullName()
				rpm_list["%s.%s" % (file.getBaseName(), \
					file.getPackageArch())] = file.getFullName()
			
		rpms = []
		for line in gen.generate('packages'):
			if line.find('%package') == -1:
				rpms.append(line)
		for rpm in rpms:
			if rpm in rpm_list.keys():
				script.append('yum install %s\n' %
					rpm)
				script.append(rpm_force_template % rpm_list[rpm])


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
		
		if dryrun:
			self.addText(string.join(script, ''))
		else:
			os.system(string.join(script, ''))

