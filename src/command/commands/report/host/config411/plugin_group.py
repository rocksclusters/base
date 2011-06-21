# $Id: plugin_group.py,v 1.1 2011/06/21 23:13:44 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: plugin_group.py,v $
# Revision 1.1  2011/06/21 23:13:44  anoop
# Without a group, 411 alerts won't work
#

import rocks.commands

class Plugin(rocks.commands.Plugin):
	def requires(self):
		return ''

	def provides(self):
		return "group"

	def run(self, args):
		# Appliance Type
		host = self.owner.s.host
		attrs = self.owner.s.attrs
		self.owner.addOutput(host, '<group>%s</group>' %\
			(attrs['membership']))
