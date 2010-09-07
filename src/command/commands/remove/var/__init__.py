# $Id: __init__.py,v 1.10 2010/09/07 23:52:58 bruno Exp $
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
# Revision 1.10  2010/09/07 23:52:58  bruno
# star power for gb
#
# Revision 1.9  2009/05/01 19:07:01  mjk
# chimi con queso
#
# Revision 1.8  2008/10/18 00:55:56  mjk
# copyright 5.1
#
# Revision 1.7  2008/03/06 23:41:39  mjk
# copyright storm on
#
# Revision 1.6  2007/07/05 17:46:45  bruno
# fixes
#
# Revision 1.5  2007/07/04 01:47:39  mjk
# embrace the anger
#
# Revision 1.4  2007/06/27 23:59:23  bruno
# more cleanup.
#
# phil, commence head shaking.
#
# Revision 1.3  2007/06/19 16:42:42  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.2  2007/06/16 00:15:04  phil
# Allow wildcarded services and components
#
# Revision 1.1  2007/06/13 05:53:49  phil
# added remove var
# (Note: our database scheme should define a global appliance).
#
# Revision 1.1  2007/06/13 05:25:20  phil
# Set a variable.
# Handle appliance specific variables (needed for CAMERA)
#
# Revision 1.3  2007/06/12 22:04:24  phil
# Change the SQL query to match the appliances lists in rocks list appliance
#
# Revision 1.2  2007/06/12 21:19:26  phil
# provide a usage.
#
# Revision 1.1  2007/06/12 21:13:53  phil
# List app_globals in the database
#
import sys
import socket
import rocks.commands

class Command(rocks.commands.remove.command):
	"""
	Removes variables in the Rocks key/value database. Variables are
	defined as a quad of (Appliance, Service, Component, Value).
	Within a node XML file, values can be retrieved as
	&lt;var name="Service_Component"/&gt;.

	<arg type='string' name='service'>
	The 'service' of the variable to remove.
	</arg>

	<arg type='string' name='component'>
	The 'component' of the variable to remove.
	</arg>
	
	<param type='string' name='service'>
	Can be used in place of service argument.
	</param>

	<param type='string' name='component'>
	Can be used in place of component argument.
	</param>

	<param type='string' name='appliance'>
	If supplied, remove the Service_Component variable that is
	associated with this appliance.
	</param>
		
	<example cmd='remove var service=Condor component=Master'>
	Remove the variable Condor_Master from the database.
	</example>

	<example cmd='remove var service=Condor component=Master appliance=compute'>
	Remove the variable Condor_Master that is associated with the
	compute appliance.
	</example>
	"""

	def run(self, params, args):
		(args, service, component) = self.fillPositionalArgs(
				('service', 'component'))

		(appliance, ) = self.fillParams([('appliance', )])

		if not service:
			self.abort('must supply service')
		if not component:
			self.abort('must supply component')
			



		## Check if value exists 
		selectQuery = "select service,component,value"
		deleteQuery = "delete"
		query = """ from app_globals where
			    	service like '%s' and 
				component like '%s'""" % (service, component)

		subquery = ""

		if appliance:
			subquery = """ and membership=(select memberships.id
                                        from memberships,appliances where 
                                        appliances.name='%s' and
					memberships.appliance = appliances.id)
					""" % (appliance)
	 	else:
			subquery = " and membership=0 "

		q1 = selectQuery + query + subquery
		rows = self.db.execute(q1)

		if rows >= 1:
			## remove if things exist
			q1 = deleteQuery + query + subquery 
			self.db.execute(q1)

