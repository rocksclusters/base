# $Id: __init__.py,v 1.10 2012/11/27 00:48:26 phil Exp $
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
# Revision 1.10  2012/11/27 00:48:26  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.9  2012/05/06 05:48:34  phil
# Copyright Storm for Mamba
#
# Revision 1.8  2011/07/23 02:30:37  phil
# Viper Copyright
#
# Revision 1.7  2011/05/10 18:35:01  anoop
# mysql does not like it if you don't quote values
#
# Revision 1.6  2011/05/10 05:12:47  anoop
# Move shadow attributes out of attributes tables.
# Seperate secure attributes table for all attributes
# that we want to hide. These attributes will never
# be passed through kickstart.
#
# Revision 1.5  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.4  2010/08/04 23:36:56  bruno
# fix
#
# Revision 1.3  2010/07/31 01:02:02  bruno
# first stab at putting in 'shadow' values in the database that non-root
# and non-apache users can't read
#
# Revision 1.2  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.1  2008/12/20 01:06:15  mjk
# - added appliance_attributes
# - attributes => node_attributes
# - rocks set,list,remove appliance attr
# - eval shell for conds has a special local dictionary that allows
#   unresolved variables (attributes) to evaluate to None
# - need to add this to solaris
# - need to move UserDict stuff into pylib and remove cut/paste code
# - need a drink
#


import os
import stat
import time
import sys
import string
import rocks.commands
import rocks.commands.set.attr
import xml.sax.saxutils


class Command(rocks.commands.set.appliance.command):
	"""
	Sets an attribute to an appliance and sets the associated values 

	<arg type='string' name='appliance'>
	Name of appliance
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

	<example cmd='set appliance attr compute sge False'>
	Sets the sge attribution to False for compute appliances
	</example>

	<example cmd='set appliance attr compute sge attr=cpus value=2'>
	same as above
	</example>
	
	<related>list appliance attr</related>
	<related>remove appliance attr</related>
	<related>set host attr</related>
	<related>list host attr</related>
	<related>remove host attr</related>
	"""

	def run(self, params, args):

		(args, attr, value) = self.fillPositionalArgs(('attr', 'value'))
		appliances = self.getApplianceNames(args)
		
		if not attr:
			self.abort('missing attribute name')
		if not value:
			self.about('missing value of attribute')

		for appliance in appliances:
			self.setApplianceAttr(appliance, attr, value)
			
	def setApplianceAttr(self, appliance, attr, value):


		if not attr.endswith(rocks.commands.set.attr.postfix):
			# escape only if it is not a _old attribute
			value = xml.sax.saxutils.escape(value)

		rows = self.db.execute("""
			select attr, value from appliance_attributes where
			appliance=
			(select id from appliances where name='%s') and
			attr='%s'
			""" % (appliance, attr))
		if not rows:
			self.db.execute("""
				insert into appliance_attributes values 
				((select id from appliances where name='%s'), 
				'%s', '%s')
				""" % (appliance, attr, value))
		else:
			(useless, old_value) = self.db.fetchone()

			self.db.execute("""update appliance_attributes
				set value = '%s' where attr = '%s' and
				appliance = (select id from appliances
				where name = '%s') """ % (value, attr,
				appliance))

			if not attr.endswith(rocks.commands.set.attr.postfix):
				self.command('set.appliance.attr',
					[appliance, attr + rocks.commands.set.attr.postfix, old_value])

