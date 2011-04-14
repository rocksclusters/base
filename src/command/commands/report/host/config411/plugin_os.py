# $Id: plugin_os.py,v 1.1 2011/04/14 23:06:24 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: plugin_os.py,v $
# Revision 1.1  2011/04/14 23:06:24  anoop
# 411 configuration now created as a report. Plugins may be added
# to put more information into the 411 configuration. This information
# will be used during 411 filters
#

import rocks.commands

class Plugin(rocks.commands.Plugin):
	def requires(self):
		return ''

	def provides(self):
		return "os"

	def run(self, args):
		# OS Type
		host = self.owner.s.host
		attrs = self.owner.s.attrs
		self.owner.addOutput(host, '<os>%s</os>' %\
			(attrs['os']))
