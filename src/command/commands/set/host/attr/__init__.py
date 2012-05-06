# $Id: __init__.py,v 1.10 2012/05/06 05:48:34 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# Revision 1.10  2012/05/06 05:48:34  phil
# Copyright Storm for Mamba
#
# Revision 1.9  2011/07/23 02:30:37  phil
# Viper Copyright
#
# Revision 1.8  2011/05/10 18:35:02  anoop
# mysql does not like it if you don't quote values
#
# Revision 1.7  2011/05/10 05:12:47  anoop
# Move shadow attributes out of attributes tables.
# Seperate secure attributes table for all attributes
# that we want to hide. These attributes will never
# be passed through kickstart.
#
# Revision 1.6  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.5  2010/07/31 01:02:02  bruno
# first stab at putting in 'shadow' values in the database that non-root
# and non-apache users can't read
#
# Revision 1.4  2009/05/01 19:07:03  mjk
# chimi con queso
#
# Revision 1.3  2008/12/20 01:06:15  mjk
# - added appliance_attributes
# - attributes => node_attributes
# - rocks set,list,remove appliance attr
# - eval shell for conds has a special local dictionary that allows
#   unresolved variables (attributes) to evaluate to None
# - need to add this to solaris
# - need to move UserDict stuff into pylib and remove cut/paste code
# - need a drink
#
# Revision 1.2  2008/12/18 20:01:33  mjk
# attribute commands
#
# Revision 1.1  2008/12/18 18:47:55  mjk
# *** empty log message ***
#


import os
import stat
import time
import sys
import string
import rocks.commands


class Command(rocks.commands.set.host.command):
	"""
	Sets an attribute to a host and sets the associated values 

	<arg type='string' name='host'>
	Host name of machine
	</arg>
	
	<arg type='string' name='attr'>
	Name of the attribute
	</arg>

	<arg type='string' name='value'>
	Value of the attribute
	</arg>
	
	<param type='string' name='attr'>
	same as attr argument
	</param>

	<param type='string' name='value'>
	same as value argument
	</param>

	<example cmd='set host attr compute-0-0 cpus 2'>
	Sets the number of cpus of compute-0-0 to 2
	</example>

	<example cmd='set host attr compute-0-0 attr=cpus value=2'>
	same as above
	</example>
	
	<related>list host attr</related>
	<related>remove host attr</related>
	"""

	def run(self, params, args):

		(args, attr, value) = self.fillPositionalArgs(('attr', 'value'))
		hosts = self.getHostnames(args)
		
		if not attr:
			self.abort('missing attribute name')
		if not value:
			self.about('missing value of attribute')

		for host in hosts:
			self.setHostAttr(host, attr, value)

			
	def setHostAttr(self, host, attr, value):
		rows = self.db.execute("""
			select * from node_attributes where
			node=(select id from nodes where name='%s') and
			attr='%s'
			""" % (host, attr))
		if not rows:
			self.db.execute("""
				insert into node_attributes values 
				((select id from nodes where name='%s'), 
				'%s', '%s')
				""" % (host, attr, value))
		else:
			self.db.execute("""update node_attributes set
				value = '%s' where attr = '%s' and
				node = (select id from nodes where
				name = '%s') """ % (value, attr, host)) 

