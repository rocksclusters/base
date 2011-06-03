# $Id: __init__.py,v 1.1 2011/06/03 02:34:39 anoop Exp $

# @Copyright@
# @Copyright@

# $ Log: $

import os
import sys
import rocks.commands

class Command(rocks.commands.remove.command):
	"""
	Delete the named attribute from the global secure attributes table
	<arg type="string" name="attr">
	The attribute you want to remove
	</arg>
	"""
	def run(self, params, args):
		(args, attr) = self.fillPositionalArgs(('attr',))

		if not attr:
			self.abort('Please specify attribute')

		self.db.execute('delete from sec_global_attributes ' +\
			'where attr="%s"' % attr)
