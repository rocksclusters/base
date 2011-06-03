# $Id: __init__.py,v 1.1 2011/06/03 02:34:40 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.1  2011/06/03 02:34:40  anoop
# Added code for secure_attributes
#


import os
import sys
import pickle

import base64
import tempfile

import rocks.commands

from rocks.commands.sync.host import Parallel
from rocks.commands.sync.host import timeout

class Command(rocks.commands.sync.host.command):
	"""
	This command syncs the secure attributes
	of a host.
	<arg name="host" type="string">
	Hostname(s) whose secure attributes
	need to be synced.
	</arg>
	"""
	def run(self, params, args):
		hosts = self.getHostnames(args, managed_only=1)
		
		attr_dict = {}
	
		# Index all available plugins by attribute
		plugin_dict = {}
		# Path where plugins are stored
		plugin_path = '/opt/rocks/var/plugins/sec_attr'
		sys.path.append(plugin_path)
		# Read all plugins in plugin path
		for plugin_file in os.listdir(plugin_path):
			if not plugin_file.endswith('.py'):
				continue
			p = plugin_file.split('.py')[0]
			# Import the plugin
			plugin = __import__(p).plugin()
			# Get the attribute that the plugin
			# will run on, and append it to the
			# plugin dictionary
			plugin_dict[plugin.get_sec_attr()] = plugin_file

		# Sync the secure information with the plugins
		threads = []
		for host in hosts:
			# Get a list of all secure attributes
			# of the host
			a_d = self.db.getHostSecAttrs(host)
			for a in a_d:
				# For each attribute, get the value
				value = a_d[a][0]

				# check if there is a plugin that
				# acts on the attribute
				plugin = None
				if plugin_dict.has_key(a):
					plugin_f = open(os.path.join(
						plugin_path, plugin_dict[a]), 'r')
					plugin = base64.b64encode(plugin_f.read())
					plugin_f.close()
				if plugin is not None:
					attr_dict[a] = (value, plugin)
			# Once we get attribute, value, and plugin
			# pickle the information for the host
			(fid, fname) = tempfile.mkstemp()
			f = open(fname, 'w')
			pickle.dump(attr_dict, f)
			f.close()
			
			# Three commands are run in a single thread so that
			# we perform them as an atomic operation.

			# Ship the pickled file to destination host
			cmd = 'scp -q %s %s:%s; ' % (fname, host, fname)
			# Remove the file from the frontend
			cmd = cmd + 'rm -rf %s; ' % (fname)
			# Run the unpickle procedure and run the plugin
			cmd = cmd + 'ssh %s ' % (host)	+\
				'"/opt/rocks/bin/rocks '+\
				'run host sec_attr %s"' % (fname)
			p = Parallel(cmd, host)
			p.start()
			threads.append(p)
			
		for thread in threads:
			thread.join(timeout)
