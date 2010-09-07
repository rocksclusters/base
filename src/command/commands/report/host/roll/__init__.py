# $Id: __init__.py,v 1.5 2010/09/07 23:53:00 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.5  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.4  2009/05/19 20:12:54  bruno
# get attributes from the host, not just the localhost
#
# Revision 1.3  2009/05/01 19:18:49  bruno
# point to the kickstart host
#
# Revision 1.2  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.1  2009/03/24 15:57:57  bruno
# report the rolls for VM frontend
#
#

import rocks.commands

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):
	"""
	Create a report in XML format for a set of rolls that should be
	applied to a frontend's configuration.

	<arg optional='1' type='string' name='host'>
	Host name of machine
	</arg>
	
	<example cmd='report host roll frontend-0-0-0'>
	Report the rolls assigned to frontend-0-0-0.
	</example>
	"""

	def run(self, params, args):
		self.beginOutput()

		fe_hosts = self.getHostnames( [ 'frontend' ] )
		hosts = self.getHostnames(args)

		for host in hosts:
			if host not in fe_hosts:
				continue

			self.addOutput(host, '<rolls>')

			public_hostname = self.db.getHostAttr(host, 
				'Kickstart_PublicKickstartHost')
			basedir = self.db.getHostAttr(host,
				'Kickstart_PrivateKickstartBasedir')

			rows = self.db.execute("""
				select r.name, r.version, r.arch from
				rolls r, node_rolls nr, nodes n where
				nr.node = n.id and n.name = '%s' and
				r.id = nr.rollid""" % (host))

			for name, ver, arch in self.db.fetchall():
				self.addOutput(host, '<roll')

				self.addOutput(host, '\tname="%s"' % name)
				self.addOutput(host, '\tversion="%s"' % ver)
				self.addOutput(host, '\tarch="%s"' % arch)
				self.addOutput(host,
					'\turl="http://%s/%s/rolls/"' %
					(public_hostname, basedir))
				self.addOutput(host, '\tdiskid=""')

				self.addOutput(host, '/>')

			self.addOutput(host, '</rolls>')

		self.endOutput(padChar='')

