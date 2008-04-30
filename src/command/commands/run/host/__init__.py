# $Id: __init__.py,v 1.3 2008/04/14 21:15:06 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
#
# $Log: __init__.py,v $
# Revision 1.3  2008/04/14 21:15:06  bruno
# let users use 'rocks run host'
#
# Revision 1.2  2008/03/06 23:41:39  mjk
# copyright storm on
#
# Revision 1.1  2008/01/29 22:13:05  bruno
# added 'rocks run host'
#
# it executes a command on all listed hosts
#
#

import rocks.commands

import lekatnet.config as config
import lekatnet.remote as remote

class RocksRemoteCollator(remote.RemoteCollator):
	def __init__(self, cmd):
		self.clear()
		self.formatter = remote.FormatString()
		self.cmd = cmd

	def displayAll(self):
		"Display the next pending result for every remote object"

		displayCount = len(self.remoteobjects)
		while displayCount > 0:
			obj = remote.RemoteCommand.finishedObjects.get()
			displayCount -= 1
			status, output = obj.getResult()

			for line in output.split('\n'):
				self.cmd.addOutput(obj.destination, line)

	
class command(rocks.commands.HostArgumentProcessor,
	rocks.commands.run.command):

	MustBeRoot = 0

	
class Command(command):
	"""
	Run a command for each specified host.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, the command
	is run on all known hosts.
	</arg>

	<arg type='string' name='command'>
	The command to run on the list of hosts.
	</arg>

	<param type='string' name='command'>
	Can be used in place of the 'command' argument.
	</param>

	<example cmd='run host compute-0-0 command="hostname"'>
	Run the command 'hostname' on compute-0-0.
	</example>

	<example cmd='run host compute "ls /tmp"'>
	Run the command 'ls /tmp/' on all compute nodes.
	</example>
	"""

	def run(self, params, args):
		(args, command) = self.fillPositionalArgs(('command', ))

		if not command:
			self.abort('must supply a command')

		hosts = self.getHostnames(args)

		conf = config.ConfigBase()
		f = open('/etc/tentakel.conf')
		conf.load(f)
		f.close()

		dests = RocksRemoteCollator(self)
		dests.format = '%o\\n'

		params = conf.getGroupParams('default')

		for host in hosts:
			dests.add(remote.remoteCommandFactory(host, params))

		dests.execAll(command)

		self.beginOutput()
		dests.displayAll()
		self.endOutput(padChar='')
		
