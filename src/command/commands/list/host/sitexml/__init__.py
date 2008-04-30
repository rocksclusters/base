# $Id: __init__.py,v 1.8 2008/03/06 23:41:38 mjk Exp $
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
# Revision 1.8  2008/03/06 23:41:38  mjk
# copyright storm on
#
# Revision 1.7  2007/09/08 06:42:39  anoop
# Added ability for commands to accept the os=something option
#
# Revision 1.6  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.5  2007/07/02 23:01:43  bruno
# only root and apache can list the profile and sitexml info
#
# Revision 1.4  2007/06/28 19:45:44  bruno
# all the 'rocks list host' commands now have help
#
# Revision 1.3  2007/06/19 16:42:42  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.2  2007/05/31 19:35:42  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.1  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.3  2007/03/28 22:33:50  mjk
# - add getHostname() method to base command class
# - fix bad try block for default args in list.node.xml
# - list.node.xml works as standalone
#
# Revision 1.2  2007/02/28 03:06:29  mjk
# - "rocks list host xml" replaces kpp
# - kickstart.cgi uses "rocks list host xml"
# - indirects in node xml now works
#
# Revision 1.1  2007/02/27 20:19:47  mjk
# *** empty log message ***
#

import sys
import socket
import rocks.commands
from xml.sax import saxutils

class Command(rocks.commands.list.host.command):
	"""
	Lists the site XML file for hosts. For each host supplied on the
	command line, this command prints the site.xml file for that host
	which is used for host configuration.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>

	<example cmd='list host sitexml compute-0-0'>
	List the site XML file for compute-0-0.
	</example>

	<example cmd='list host sitexml'>
	List the site XML file for all known hosts.
	</example>
	"""

	MustBeRoot = 1

	def dumpSiteXML(self, host):

		# Build a sorted list of all the key,value pairs in the
		# app_globals table, with all the indirects already
		# resolved.
		
		list = []
		self.db.execute('select distinct service from app_globals')
		for service, in self.db.fetchall():
			dict = self.db.getGlobalVars(service, host)
			for (key, val) in dict.items():
				list.append(('%s_%s' % 
					(service, key), saxutils.escape(val)))
		list.sort()
		
		if self.os == 'sunos':
			starter_tag = 'jumpstart'
		else:
			starter_tag = 'kickstart'
			
		self.addOutput(host, '<%s>' % starter_tag)
		for e in list:
			self.addOutput(host, '\t<var name="%s" val="%s"/>' % 
				(e[0], e[1]))
		self.addOutput(host, '</%s>' % starter_tag)
		
		
	def run(self, params, args):
		
		if params.has_key('os'):
			self.os = params['os']
			
		self.beginOutput()
		for host in self.getHostnames(args):
			self.dumpSiteXML(host)
		self.endOutput(padChar='')

