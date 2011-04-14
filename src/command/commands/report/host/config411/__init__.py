# $Id: __init__.py,v 1.1 2011/04/14 23:06:24 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.1  2011/04/14 23:06:24  anoop
# 411 configuration now created as a report. Plugins may be added
# to put more information into the 411 configuration. This information
# will be used during 411 filters
#

import rocks.commands
import rocks.util

class Command(rocks.commands.report.host.command):
	"""This command outputs the 411 config file
	for a particular host"""
	def run(self, params, args):
		hosts = self.getHostnames(args)
		self.beginOutput()
		self.s = rocks.util.Struct()
		file_ent = '<file name="/etc/411.conf" perms="0600" owner="root:root">'
		cdata_ent = '<![CDATA[<!-- 411 Configuration -->'
		for host in hosts:
			attrs = self.db.getHostAttrs(host)
			
			self.addOutput(host, file_ent)
			self.addOutput(host, cdata_ent)
			self.addOutput(host, '<config>')
			# Run Plugins
			self.s.host = host
			self.s.attrs = attrs
			self.runPlugins()

			self.addOutput(host, '</config>')
			self.addOutput(host, ']]>')

			self.addOutput(host, '</file>')

		self.endOutput()
