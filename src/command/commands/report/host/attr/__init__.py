# $Id: __init__.py,v 1.12 2012/11/27 00:48:24 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.12  2012/11/27 00:48:24  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.11  2012/05/06 05:48:32  phil
# Copyright Storm for Mamba
#
# Revision 1.10  2012/05/05 16:38:28  phil
# When printing a python dictionary, suppress newline
#
# Revision 1.9  2012/03/13 06:09:02  phil
# Be more tolerant -- or don't emit errors in particular benign cases
#
# Revision 1.8  2011/07/23 02:30:35  phil
# Viper Copyright
#
# Revision 1.7  2011/03/24 19:37:00  phil
# Wrap routes report inside of XML tag to make it like interfaces,networks.
# Add ability to report host addr to output a python dictionary
# mod routes-*.xml and sync host network to use new output format
#
# Revision 1.6  2010/09/07 23:52:59  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:07:01  mjk
# chimi con queso
#
# Revision 1.4  2009/03/06 00:26:17  mjk
# *** empty log message ***
#
# Revision 1.3  2009/03/06 00:21:52  mjk
# added attr param
#
# Revision 1.2  2009/03/04 20:15:31  bruno
# moved 'dbreport hosts' and 'dbreport resolv' into the command line
#
# Revision 1.1  2009/03/03 22:40:32  mjk
# - remove list.host.sitexml
# - added  report.host.attr
#

import sys
import socket
import rocks.commands
import string

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""
	Report the set of attributes for hosts.

	<arg optional='1' type='string' name='host'>
	Host name of machine
	</arg>

	<param optional='1' type='string' name='attr'>
	Output just the value of a particular attribute	
	</param>
	
	<param optional='1' type='bool' name='pydict'>
	Output as a python-formatted dictionary. Defaults to false.
	Only valid if attr parameter is not specified.
	</param>
	
	<example cmd='report host attr compute-0-0'>
	Report the attributes for compute-0-0.
	</example>

	<example cmd='report host attr compute-0-0 pydict=true'>
	Report the attributes for compute-0-0 as a python dictionary suitable
	for input to rocks report script.
	</example>

	<example cmd='report host attr compute-0-0 attr=Kickstart_Lang'>
	Output value of the attribute called Kickstart_Lang for node
	compute-0-0.
	</example>

	<related>report script</related>
	"""

	def run(self, params, args):

		(attr, pydict) = self.fillParams([('attr', ),('pydict','false')])
		pyformat=self.str2bool(pydict)

		self.beginOutput()
		
		try:
			for host in self.getHostnames(args):
	
				if not attr:
					if pyformat:
						fmt="'%s':'%s',"
					else:
						fmt="%s:%s"
					attrs = self.db.getHostAttrs(host)
					keys = attrs.keys()
					keys.sort()
					if pyformat:
						self.addOutput(host, '{')
					for key in keys:
						self.addOutput(host,
							fmt % (key, attrs[key]))
					if pyformat:
						self.addOutput(host,'}')
				else:
					self.addOutput(host,
						self.db.getHostAttr(host, attr))
	
		except:
			pass

		if pyformat:
			self.endOutput(padChar='',linesep='')
		else:
			self.endOutput(padChar='')

