# $Id: __init__.py,v 1.12 2012/11/27 00:48:26 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# Revision 1.12  2012/11/27 00:48:26  phil
# Copyright Storm for Emerald Boa
#
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
	It generates the code necessary to install a Roll on the fly

	<arg optional='1' type='string' name='roll' repeat='1'>
	List of rolls. This should be the roll base name (e.g., base, hpc,
	kernel).
	</arg>

	<param type='string' name='host'>
	The name of the host that you want to generate the code to install the Roll.
	It is always better to reinstall the node instead of using this method.
	</param>

	<param type='string' name='dryrun'>
	It runs the command on the current node. It doesn't work with host flag
	Default: true
	</param>

	<example cmd='run roll viz'>
	It generates the bash code necessary to install the Viz Roll onto the current system.
	</example>

	<example cmd='run roll viz host=compute-0-0'>
	It generates the bash code necessary to install the Viz Roll on compute-0-0.
	</example>
	"""

	def run(self, params, args):

		(dryrun, host ) = self.fillParams([('dryrun', None),
						   ('host', None)])
		
		if dryrun:
			dryrun = self.str2bool(dryrun)
			if not dryrun and host:
				self.abort("If you select a host you can't disable dryrun.")
		else:
			dryrun = True

		if not host:
			host = 'localhost'

		script = []
		script.append('#!/bin/sh\n')
		script.append('yum clean all\n')
			
		rolls = []
		for roll in args:
			rolls.append(roll)
		xml = self.command('list.host.xml', [ host,
			'roll=%s' % string.join(rolls, ',') ])


		reader = Sax2.Reader()
		gen = getattr(rocks.gen,'Generator_%s' % self.os)()
		gen.setArch(self.arch)
		gen.setOS(self.os)
		gen.parse(xml)

		distPath = os.path.join(self.command('report.distro')[:-1], 'rocks-dist')
                tree = rocks.file.Tree(distPath)
		rpm_list = {}
		len_base_path = len('/export/rocks')
                base_url = "http://" + self.db.getHostAttr('localhost', 'Kickstart_PublicHostname')
		for file in tree.getFiles(os.path.join(self.arch, 'RedHat', 'RPMS')):
			if isinstance(file, rocks.file.RPMFile):
				rpm_url = base_url + file.getFullName()[len_base_path:]
				rpm_list[file.getBaseName()] = rpm_url
				rpm_list["%s.%s" % (file.getBaseName(), \
					file.getPackageArch())] = rpm_url
			
		rpms = []
		for line in gen.generate('packages'):
			if line.find('%package') == -1:
				rpms.append(line)
		for rpm in rpms:
			if rpm in rpm_list.keys():
				script.append('yum install %s\n' % rpm)
				script.append(rpm_force_template % rpm_list[rpm])

		script += gen.generate_config_script()
		
		if dryrun:
			self.addText(string.join(script, ''))
		else:
			os.system(string.join(script, ''))


RollName = "base"
