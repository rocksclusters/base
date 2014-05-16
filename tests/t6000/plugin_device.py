#!/opt/rocks/bin/python
# 
#

import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return '%PLUGINNAME%'

	def run(self, node, xml):
		"""report host vm config xml filter"""
		xml.append('<plugin_' + self.provides() + '/>')
		return xml


