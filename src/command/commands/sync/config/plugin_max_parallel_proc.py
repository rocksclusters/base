# $Id: plugin_max_parallel_proc.py,v 1.1 2011/04/21 02:32:38 anoop Exp $

# @Copyright@
# @Copyright@
 
# $Log: plugin_max_parallel_proc.py,v $
# Revision 1.1  2011/04/21 02:32:38  anoop
# maximum allowable parallel processes are now
# a configuration variable on the frontend. Can
# be set and changed during runtime.
#

import rocks.commands

class Plugin(rocks.commands.Plugin):
	def provides(self):
		return 'max-parallel-proc'
		

	def run(self, args):
		m = self.db.getHostAttr('localhost','max_parallel_proc')
		if m is None:
			return
		f = open('/var/lock/rocks-sync-host.lock','w+')
		f.write('%04d\n' % int(m))
		f.close()
