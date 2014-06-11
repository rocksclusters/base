# $Id: __init__.py,v 1.7 2012/11/27 00:48:16 phil Exp $
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
# Revision 1.7  2012/11/27 00:48:16  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.6  2012/05/06 05:48:25  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2011/07/23 02:30:29  phil
# Viper Copyright
#
# Revision 1.4  2010/09/07 23:52:54  bruno
# star power for gb
#
# Revision 1.3  2010/05/20 00:31:45  bruno
# gonna get some serious 'star power' off this commit.
#
# put in code to dynamically configure the static-routes file based on
# networks (no longer the hardcoded 'eth0').
#
# Revision 1.2  2009/05/01 19:06:57  mjk
# chimi con queso
#
# Revision 1.1  2009/03/13 20:34:19  mjk
# - added list.appliance.route
# - added list.os.route
#

import sys
import socket
import rocks.commands
import string

class Command(rocks.commands.list.appliance.command):
	"""
	Lists routes associated with a set of appliances

	<arg optional='1' type='string' name='appliance'>
	Name of appliance (can be also a sql regexp)
	</arg>

	<example cmd='list appliance route compute'>
	List the routes for compute appliance
	</example>
	"""

	def run(self, params, args):

		self.beginOutput()

		for app in self.newdb.getApplianceNames(args):
			self.db.execute("""
				select r.network, r.netmask, r.gateway,
				r.subnet from appliance_routes r, appliances a
				where r.appliance=a.id and a.name='%s'""" % app.name)

			for network,netmask,gateway,subnet in \
				self.db.fetchall():

				if subnet:
					rows = self.db.execute("""select name
						from subnets where id = %s"""
						% subnet)
					if rows == 1:
						gateway, = self.db.fetchone()

				self.addOutput(app.name, (network, netmask, gateway))

		self.endOutput(header=['appliance', 'network', 
			'netmask', 'gateway' ], trimOwner=0)


RollName = "base"
