# $Id: __init__.py,v 1.8 2011/07/23 02:30:27 phil Exp $
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
# Revision 1.8  2011/07/23 02:30:27  phil
# Viper Copyright
#
# Revision 1.7  2010/09/07 23:52:52  bruno
# star power for gb
#
# Revision 1.6  2009/06/19 21:07:27  mjk
# - added dumpHostname to dump commands (use localhost for frontend)
# - added add commands for attrs
# - dump uses add for attr (does not overwrite installer set attrs)A
# - do not dump public or private interfaces for the frontend
# - do not dump os/arch host attributes
# - fix various self.about() -> self.abort()
#
# Revision 1.5  2009/05/01 19:06:56  mjk
# chimi con queso
#
# Revision 1.4  2009/03/24 18:50:21  bruno
# fixes for new database schema
#
# Revision 1.3  2008/12/23 00:14:05  mjk
# - moved build and eval of cond strings into cond.py
# - added dump appliance,host attrs (and plugins)
# - cond values are typed (bool, int, float, string)
# - everything works for client nodes
# - random 80 col fixes in code (and CVS logs)
#
# Revision 1.2  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.1  2008/07/31 22:06:29  bruno
# added 'rocks dump appliance'
#
#

import os
import sys
import string
import rocks.commands

class command(rocks.commands.ApplianceArgumentProcessor,
	rocks.commands.dump.command):
	pass

class Command(command):
	"""
	Outputs info (as rocks commands) about the appliances defined in the
	cluster database.
	
	<arg optional='1' type='string' name='appliance' repeat='1'>
	Optional list of appliance names. If no appliance names are supplied,
	then info about all appliances is output.
	</arg>
		
	<example cmd='dump appliance'>
	Dump all known appliances.
	</example>
	"""

	def run(self, params, args):
		for app in self.getApplianceNames(args):
			self.db.execute("""select graph, node from appliances
				where name='%s'""" % app)

			(graph, node) = self.db.fetchone()

			self.db.execute("""select m.name, m.public
				from memberships m, appliances a where
				m.appliance = a.id and a.name = '%s'""" % (app))

			(mem, pub) = self.db.fetchone()

			str = "add appliance %s " % app

			if graph and graph != 'NULL':
				str += "graph=%s " % graph
			if node and node != 'NULL':
				str += "node=%s " % node
			if mem:
				str += "membership=%s " % self.quote(mem)
			if pub:
				str += "public=%s" % pub
				
			self.dump(str)

