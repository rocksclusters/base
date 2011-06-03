# $Id: __init__.py,v 1.1 2011/06/03 02:34:39 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.1  2011/06/03 02:34:39  anoop
# Added code for secure_attributes
#

import os
import sys
import rocks.commands
import string

class Command(rocks.commands.list.host.command):
	"""
	Lists the secure attributes for a given host
	<arg name="host" type="string">
	Hostname(s)
	</arg>
	"""
	def run(self, params, args):
		hosts = self.getHostnames(args)
		self.beginOutput()
		for host in hosts:
			s_a = self.db.getHostSecAttrs(host)
			for attr in s_a:
				self.addOutput(host, (attr, s_a[attr][0], s_a[attr][1]))
		self.endOutput(header=['host','attr', 'value', 'enc'])
			
