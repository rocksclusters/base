# $Id: __init__.py,v 1.10 2011/07/23 02:30:30 phil Exp $
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
# Revision 1.10  2011/07/23 02:30:30  phil
# Viper Copyright
#
# Revision 1.9  2011/06/06 15:02:31  phil
# add parameter to limit maxwidth of comment and flags field for easier reading
#
# Revision 1.8  2011/06/02 21:49:35  phil
# Update to new firewall resolution method
#
# Revision 1.7  2010/11/23 20:55:57  bruno
# we need to list rules that are exactly the same 'except' for their 'flags'
# field.
#
# Revision 1.6  2010/09/07 23:52:55  bruno
# star power for gb
#
# Revision 1.5  2010/05/27 00:11:32  bruno
# firewall fixes
#
# Revision 1.4  2010/05/11 22:28:16  bruno
# more tweaks
#
# Revision 1.3  2010/05/07 23:13:32  bruno
# clean up the help info for the firewall commands
#
# Revision 1.2  2010/05/04 22:04:15  bruno
# more firewall commands
#
# Revision 1.1  2010/04/30 22:07:16  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#

import rocks.commands

class Command(rocks.commands.NetworkArgumentProcessor,
	rocks.commands.list.host.command):
	"""
	List the current firewall rules for the named hosts.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, the 
	firewall rules for all the known hosts are listed.
	</arg>

	<param type='integer' name='maxwidth' optional='1'>
	Maximum width of comment and flags field. Default is 24.
	</param>

	"""


	def run(self, params, args):
		self.beginOutput()

		(maxwidth,) = self.fillParams([('maxwidth',24),])
		maxwidth = int(maxwidth)

		for host in self.getHostnames(args):
			# """ Get all rules """
			rules = {}
			comments = {}
	
			# Use stored procedure to create this host's TEMPTABLES.fwresolved with
			# rules resolved from all levels. Get all rules except NAT
	
			self.db.execute("""CALL resolvefirewalls('%s','default')""" % host)
			self.db.execute("""SELECT rulename, categoryName, insubnet, outsubnet, service,
				protocol, action, chain, flags, comment
				FROM TEMPTABLES.fwresolved ORDER BY rulename""" )

			for rulename, catname, i, o, s, p, c, a, f, cmt in self.db.fetchall():
				network = self.getNetworkName(i)
				output_network = self.getNetworkName(o)
			 	if f is not None: f = f[0:maxwidth]
				if cmt is not None: cmt = cmt[0:maxwidth]

				self.addOutput('',(rulename, s, p, c, a, network,
					output_network, f, cmt, '%s' % (catname)))
	
		self.endOutput(header=['', 'rulename', 'service', 'protocol', 'chain',
			'action', 'network', 'output-network', 'flags',
			'comment', 'category'])

