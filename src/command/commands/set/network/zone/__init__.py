#@PYTHON@

# $Id: __init__.py,v 1.1 2010/06/30 17:37:33 anoop Exp $

# @Copyright@
# @Copyright@

# 

import rocks.commands

class Command(rocks.commands.NetworkArgumentProcessor,
	rocks.commands.set.command):
	"""
	Set the zone/domain name associated with a subnet
	<arg name='network' type='string'>
	Network Name
	</arg>
	<arg name='zone' type='string'>
	Zone / Domain that the network belongs to.
	Example: optiputer.net
	</arg>
	<param name='zone' type='string'>
	Zone / Domain that the network belongs to.
	Example: optiputer.net
	</param>
	"""
	def run(self, params, args):
		args, zone = self.fillPositionalArgs(('zone',))
		if len(args) != 1:
			self.abort('must supply a network')
		if not zone:
			self.abort('must supply zone')

		network = self.getNetworkNames(args)[0]
		r = self.db.execute('select name from subnets ' +\
			'where dnszone="%s"' % zone)
		if r > 0:
			n, = self.db.fetchone()
			if n is not network:
				self.abort('zone %s already exists' % zone)

		self.db.execute('update subnets '	+\
			'set dnszone="%s" ' % zone	+\
			'where name="%s"' % network)
