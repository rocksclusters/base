# $Id: __init__.py,v 1.1 2011/06/03 02:34:39 anoop Exp $

# @Copyright@
# @Copyright@

# $ Log: $

import os
import sys
import rocks.commands

class Command(rocks.commands.remove.host.command):
	"""
	Delete an host specific named attribute from secure attributes table
	<arg type="string" name="host">
	Host name
	</arg>
	<arg type="string" name="attr">
	The attribute you want to remove
	</arg>
	"""
	def run(self, params, args):
		(args, attr) = self.fillPositionalArgs(
			('attr',))
		
		hosts = self.getHostnames(args)

		if not hosts:
			self.abort('Please specify host')

		if not attr:
			self.abort('Please specify attribute')

		for host in hosts:
			self.db.execute('delete from sec_node_attributes ' +\
				'where attr="%s" and node=' % attr	+\
				'(select id from nodes where name="%s")' % host)
