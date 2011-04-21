# $Id: plugin_master.py,v 1.2 2011/04/21 00:43:39 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: plugin_master.py,v $
# Revision 1.2  2011/04/21 00:43:39  anoop
# As Phil so eloquently put it, "Who woulda thunk that"
#
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
		return 'master'

	def run(self, args):
		# Master Server
		host = self.owner.s.host
		attrs = self.owner.s.attrs

		port_string = ''
		if attrs.has_key('port411'):
			port_string = ':%s' % attrs['port411']

		master = '<master url="http://%s%s/%s"/>' \
			% (attrs['Kickstart_PrivateAddress'],
			port_string,
			'411.d/')
		self.owner.addOutput(host, master)

		
