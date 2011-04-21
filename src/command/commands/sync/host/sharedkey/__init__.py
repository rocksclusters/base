# $Id: __init__.py,v 1.2 2011/04/21 02:31:39 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.2  2011/04/21 02:31:39  anoop
# sync commands now take advantage of new parallel class
#
# Revision 1.1  2011/04/14 23:08:59  anoop
# Move parallel class up one level, so that all sync commands can
# take advantage of it.
#
# Added rocks sync host sharedkey. This distributes the 411 shared key
# to compute nodes
#

import rocks.commands
from rocks.commands.sync.host import Parallel
from rocks.commands.sync.host import timeout


class Command(rocks.commands.sync.host.command):
	"""This command syncs the shared 411 key 
	on a particular host"""

	def run(self, params, args):
		# Get hostnames from args
		hosts = self.getHostnames(args)

		fname = '/etc/411-security/shared.key'


		# Copy the 411 shared key to all nodes
		threads = []
		for host in hosts:
			cmd = 'scp -q %s root@%s:%s' % \
				(fname, host, fname)
			p = Parallel(cmd, host)
			p.start()
			threads.append(p)

		for thread in threads:
			thread.join(timeout)
