# $Id: __init__.py,v 1.5 2009/05/01 19:06:55 mjk Exp $
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
# Revision 1.5  2009/05/01 19:06:55  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:48  mjk
# copyright 5.1
#
# Revision 1.3  2008/03/06 23:41:35  mjk
# copyright storm on
#
# Revision 1.2  2007/07/04 01:47:37  mjk
# embrace the anger
#
# Revision 1.1  2007/06/27 23:59:23  bruno
# more cleanup.
#
# phil, commence head shaking.
#
#

import sys
import socket
import rocks.commands

class Command(rocks.commands.add.command):
	"""
	Add variables to the Rocks key/value database. Variables are
	defined as quad of (Appliance, Service, Component, Value). 
	Within a node XML file, values can be retrieved as
	&lt;var name="Service_Component"/&gt;.

	<arg type='string' name='service'>
	Defines the service name. e.g., service=Kickstart.
	</arg>

	<arg type='string' name='component'>
	Defines the component name. e.g. component=PublicDNS.
	</arg>
	
	<arg type='string' name='value'>
	Defines the value for the variable.
	</arg>

	<param type='string' name='service'>
	Can be used in place of service argument.
	</param>

	<param type='string' name='component'>
	Can be used in place of component argument.
	</param>

	<param type='string' name='value'>
	Can be used in place of value argument.
	</param>

	<param type='string' name='appliance'>
	If supplied, restricts to the named appliance.
	See 'rocks list appliance' for a listing of appliances.
	</param>
		
	<example cmd='add var service=Condor component=Master value=localhost'>
	Add the variable name &lt;var name="Condor_Master"/&gt; to 'localhost'.
	</example>

	<example cmd='add var Condor Master localhost'>
	Same as above.
	</example>

	<example cmd='add var service=Condor component=Master value=localhost appliance=compute'>
	Add the variable name &lt;var name="Condor_Master"/&gt; to 'localhost'
	and associate it with only compute appliances.
	</example>
	"""

	def run(self, params, args):
		(args, service, component, value) = self.fillPositionalArgs(
				('service', 'component', 'value'))

		(appliance, ) = self.fillParams([('appliance', )])

		if not (service and component and value):
			self.abort('must supply service, component, value')


		query = """select service,component,value from app_globals 
			where service='%s' and  component='%s'""" % \
			(service, component)
		if appliance:
			query += """ and membership=
				(select m.id from
				memberships m, appliances a where
				a.name='%s' and m.appliance=a.id)""" % \
				appliance
		rows = self.db.execute(query)
		if rows > 0:
			self.abort('var "%s/%s" exists' % (service, component))


		if appliance:
			self.db.execute("""insert into app_globals
				(membership, service, component, value) values
				((select m.id from 
				memberships m, appliances a where 
				a.name='%s' and m.appliance=a.id),
				'%s','%s', '%s')""" % 
				(appliance, service, component, value))
		else:
			self.db.execute("""insert into app_globals
				(membership, service, component, value) values
				(0, '%s', '%s', '%s')""" %
				(service, component, value))

