# $Id: __init__.py,v 1.22 2011/07/23 02:30:31 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.22  2011/07/23 02:30:31  phil
# Viper Copyright
#
# Revision 1.21  2010/09/07 23:52:56  bruno
# star power for gb
#
# Revision 1.20  2010/07/07 02:10:50  anoop
# Cleanup of code. We no longer need to provide the "os" param
# if hostname is present
#
# Revision 1.19  2009/05/01 19:06:58  mjk
# chimi con queso
#
# Revision 1.18  2009/04/22 22:13:40  mjk
# - boot section works
# - still needs rc.d scripts to trigger the code
#
# Revision 1.17  2009/04/22 21:31:35  mjk
# added boot section
#
# Revision 1.16  2008/10/18 00:55:50  mjk
# copyright 5.1
#
# Revision 1.15  2008/03/06 23:41:37  mjk
# copyright storm on
#
# Revision 1.14  2007/11/27 01:27:49  anoop
# Added support for os attribute to graph and node XML files.
#
# Revision 1.13  2007/09/08 06:42:39  anoop
# Added ability for commands to accept the os=something option
#
# Revision 1.12  2007/09/02 06:45:31  anoop
# The command line to generate the profile XML made a little more flexible.
# The all new Pylib - Now with more XML tags support!!!
#
# Revision 1.11  2007/08/14 20:14:23  anoop
# Fitting pylib and the command line with solaris
# mechs
#
# Revision 1.10  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.9  2007/07/02 23:01:43  bruno
# only root and apache can list the profile and sitexml info
#
# Revision 1.8  2007/06/28 19:45:44  bruno
# all the 'rocks list host' commands now have help
#
# Revision 1.7  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.6  2007/05/31 19:35:42  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.5  2007/05/11 18:33:15  mjk
# - fix list host profiles
# - [hosts] -> [host(s)]
#
# Revision 1.4  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.3  2007/03/29 00:16:30  mjk
# - added self.os to base command
# - list.host.profile ready for solaris code
#
# Revision 1.2  2007/02/27 01:53:58  mjk
# - run(self, args) => run(self, flags, args)
# - replaced rocks list host xml with more complete code
# - replaced rocks lust node xml with kpp shell (not a command now)
#
# Revision 1.1  2007/01/12 20:18:05  anoop
# Shuffling things around a little bit
#
# From now on "node" always refers to xml files in the nodes/ directory
# Any host information that needs to be obtained should be put into
# host/ directory
#
# Revision 1.1  2007/01/10 18:06:55  mjk
# *** empty log message ***
#

import os
import sys
import popen2
import rocks.commands
import rocks.gen


class Command(rocks.commands.list.host.command):
	"""
	Outputs a XML wrapped Kickstart/Jumpstart profile for the given hosts.
	If not, profiles are listed for all hosts in the cluster. If input is
	fed from STDIN via a pipe, the argument list is ignored and XML is
	read from STDIN.  This command is used for debugging the Rocks
	configuration graph.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>

	<example cmd='list host profile compute-0-0'>
	Generates a Kickstart/Jumpstart profile for compute-0-0.
	</example>

	<example cmd='list host xml compute-0-0 | rocks list host profile'>
	Does the same thing as above but reads XML from STDIN.
	</example>
	"""

	MustBeRoot = 1

	def runXML(self, xml, host=None):
			
		# This decision should really be based on the OS of the
		# node, not the processing machine.  Keep as is until
		# an OS field is in the nodes table.

		self.addOutput(host, '<?xml version="1.0" standalone="no"?>')
		f = getattr(self, "run_%s" % self.os)
		f(xml, host)

	def run_linux(self, xml, host):
		"""Reads the XML host profile and outputs a RedHat 
		Kickstart file."""

		list = []
		self.generator.parse(xml)
		for section in [
			'order',
			'debug',
			'main',
			'packages',
			'pre',
			'post',
			'boot',
			'installclass'
			]:
			list += self.generator.generate(section)
			
		self.addOutput(host, '<profile lang="kickstart">')
		self.addOutput(host, '<section name="kickstart">')
		self.addOutput(host, '<![CDATA[')
		for line in list:
			self.addOutput(host, line.rstrip())
		self.addOutput(host, ']]>')
		self.addOutput(host, '</section>')
		self.addOutput(host, '</profile>')


	def run_sunos(self, xml, host):
		"""Reads the XML host profile and outputs Solaris
		Jumpstart files."""
		
		# This method should addText something like
		#
		# <profile lang="jumpstart">
		# <section name="file-type-a"/>
		# <![CDATA[
		# ]]>
		# </section>
		# <section name="file-type-b"/>
		# <![CDATA[
		# ]]>
		# </section>
		# ...
		# </profile>
		#
		# This keeps everything in one command and the
		# output can easily be parsed and split into 
		# individual files.
		
		self.generator.parse(xml)
		self.addOutput(host, '<profile lang="jumpstart">\n')
		self.get_section = []
		if self.section == 'all':
			self.get_section = [
			"begin",
			"profile",
			"sysidcfg",
			"finish",
			"rules",
			]
		else:
			self.get_section.append(self.section)
		for section in self.get_section:
			list = []
			list = self.generator.generate(section)
			self.addOutput(host, "<section name=\"%s\">" % section)
			self.addOutput(host, "<![CDATA[")
			for line in list:
				self.addOutput(host, line.rstrip())
			self.addOutput(host, "]]>")
			self.addOutput(host, "</section>")
		self.addOutput(host, '</profile>\n')
		
	def run(self, params, args):
		"""Generate the OS specific profile file(s) is a single XML
		stream (e.g. Kickstart or Jumpstart).  If a host argument
		is provide use it, otherwise assume the cooked XML is
		on stdin."""

		# By default, print all sections of kickstart/jumpstart file
		self.section = 'all'

		if params.has_key('section'):
			self.section = params['section']

		self.beginOutput()
		# If we're reading from stdin assume os=linux unless
		# otherwise specified
		if not sys.stdin.isatty():
			if params.has_key('os'):
				self.os = params['os']
			else:
				self.os = 'linux'
			xml = ''
			for line in sys.stdin.readlines():
				xml += line

			c_gen = getattr(rocks.gen,'Generator_%s' % self.os)
			self.generator = c_gen()
			self.generator.setArch(self.arch)
			self.generator.setOS(self.os)
			self.runXML(xml)
		
		else:		
			for host in self.getHostnames(args):
				self.os = self.db.getHostAttr(host, 'os')
				c_gen = getattr(rocks.gen,'Generator_%s' % self.os)
				self.generator = c_gen()
				self.generator.setArch(self.arch)
				self.generator.setOS(self.os)
				xml = self.command('list.host.xml', 
				[
				 host,
				 'os=%s' % self.os,
				])
				self.runXML(xml, host)
			
		self.endOutput(padChar='')	
