# $Id: __init__.py,v 1.5 2012/11/27 00:48:31 phil Exp $

# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.5  2012/11/27 00:48:31  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/07/31 23:20:10  phil
# Generate a cluster-wide ssh [rsa,dsa] keys and put them in
# the secure attributes database. These are different from frontend's host keys.
# Place these on nodes with rocks sync host sec_attr (new sec_attr plugins).
# Add list global sec_attr command
#
# Revision 1.3  2012/05/06 05:48:38  phil
# Copyright Storm for Mamba
#
# Revision 1.2  2011/07/23 02:30:41  phil
# Viper Copyright
#
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

		# create a known hosts temporary file
		# this is so we don't contaminate the regular known hosts file	
		# since this sync might change the host keys.
		(khfid, khfname) = tempfile.mkstemp()

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
			cmd = 'scp -q -o UserKnownHostsFile=%s %s %s:%s; ' % (khfname, fname, host, fname)
			# Remove the file from the frontend
			cmd = cmd + 'rm -rf %s; ' % (fname)
			# Run the unpickle procedure and run the plugin
			cmd = cmd + 'ssh -o UserKnownHostsFile=%s %s ' % (khfname,host)	+\
				'"/opt/rocks/bin/rocks '+\
				'run host sec_attr %s"' % (fname)
			p = Parallel(cmd, host)
			p.start()
			threads.append(p)
			
		for thread in threads:
			thread.join(timeout)

		if os.path.exists(khfname):
			os.unlink(khfname)
