#@PYTHON@

# $Id: __init__.py,v 1.1 2010/06/30 17:37:33 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.1  2010/06/30 17:37:33  anoop
# Overhaul of the naming system. We now support
# 1. Multiple zone/domains
# 2. Serving DNS for multiple domains
# 3. No FQDN support for network names
#    - FQDN must be split into name & domain.
#    - Each piece information will go to a
#      different table
# Hopefully, I've covered the basics, and not broken
# anything major
#

import rocks.commands

class Command(rocks.commands.NetworkArgumentProcessor,
	rocks.commands.set.command):
	"""
	Sets/Unsets the capability for serving DNS
	for a given subnet
	<arg name='network' type='string'>
	Name of the Network
	</arg>
	<arg name='servedns' type='bool'>
	True/False
	</arg>
	<param name='servedns' type='bool'>
	True/False
	</param>
	
	"""
	def run(self, params, args):
		(args,servedns) = self.fillPositionalArgs(('servedns',))
		if len(args) < 1:
			self.abort('must supply network name')

		servedns = self.str2bool(servedns)
		for network in self.getNetworkNames(args):
			self.db.execute('update subnets set '	+\
				'servedns=%s ' % servedns	+\
				'where name="%s"' % network)
