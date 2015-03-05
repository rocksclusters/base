# $Id: __init__.py,v 1.26 2012/11/27 00:48:26 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
# Revision 1.26  2012/11/27 00:48:26  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.25  2012/07/31 00:10:40  clem
# rocks run host now behaves in the same way whether it runs locally or on a
# remote node
#
# Revision 1.24  2012/05/08 01:08:34  clem
# Too many quotes (when running rocks run host localhost "ls -l" was throwing
# an IOException)
#
# Revision 1.23  2012/05/06 05:48:33  phil
# Copyright Storm for Mamba
#
# Revision 1.22  2012/04/09 21:33:18  phil
# Test for running locally. If so, simply run the command.
#
# Revision 1.21  2011/07/23 02:30:37  phil
# Viper Copyright
#
# Revision 1.20  2010/10/14 15:55:53  phil
# Pay attention to the "primary_net" attribute of the node and
# ssh to the node on that interface.
#
# Revision 1.19  2010/09/28 22:05:04  bruno
# doc fix
#
# Revision 1.18  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.17  2010/09/01 01:16:00  anoop
# Oops!!
#
# Revision 1.16  2010/09/01 01:14:48  anoop
# Use the command parameter, not the first arg on the command line
#
# Revision 1.15  2010/07/30 19:43:15  bruno
# fix up rocks run host to properly mark down nodes
#
# Revision 1.14  2010/07/20 19:32:38  bruno
# added 'num-threads' parameter
#
# Revision 1.13  2010/05/25 22:42:16  bruno
# fix 'arg' and 'param' in help
#
# Revision 1.12  2010/05/19 20:29:57  bruno
# fix
#
# Revision 1.11  2010/04/19 19:44:14  bruno
# added:
#
# - if "timeout == 0", then wait forever
#
# - if the user hits ctrl-c, then kill all the ssh processes associated with
#   the command. the ssh processes are killed on the local side (e.g., the
#   frontend), not the remote side
#
# Revision 1.10  2010/04/15 19:00:30  bruno
# 'rocks run host' is now 100% tentakel free!
#
# Revision 1.9  2010/02/24 22:04:25  bruno
# added a 'timeout' parameter to 'rocks run host'. idea by Tim Carlson.
#
# Revision 1.8  2009/07/13 19:34:31  bruno
# fix 'managed' flag
#
# Revision 1.7  2009/06/03 18:53:43  mjk
# - sudo support for ubuntu boy (this is cool)
# - connect to DB over the network socket not the UNIX domain socket
# - added x11 param to rocks.run.host to disable x11forwarding
#
# Revision 1.6  2009/05/27 20:15:28  bruno
# add 'managed' flag
#
# Revision 1.5  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:57  mjk
# copyright 5.1
#
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

import threading
import os
import sys
import time
import socket
import subprocess
import rocks.commands

class Parallel(threading.Thread):
	def __init__(self, cmdclass, cmd, host, hostif, stats, collate):
		threading.Thread.__init__(self)
		self.cmd = cmd
		self.host = host
		self.hostif = hostif
		self.stats = stats
		self.collate = collate
		self.cmdclass = cmdclass

	def run(self):
		starttime = time.time()
		self.p = subprocess.Popen(self.cmd,
			stdin = subprocess.PIPE, stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT)

		for line in self.p.stdout.readlines():
			if self.collate:
				self.cmdclass.addOutput(self.host, line[:-1])
			else:
				print line[:-1]

		if self.stats:
			msg = 'command on host %s took %f seconds' % \
				(self.host, time.time() - starttime)

			if self.collate:
				self.cmdclass.addOutput(self.host, msg)
			else:
				print msg

	def kill(self):
		os.kill(self.p.pid, 9)

	
class command(rocks.commands.HostArgumentProcessor,
	rocks.commands.run.command):

	MustBeRoot = 0

	
class Command(command):
	"""
	Run a command for each specified host.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, the command
	is run on all 'managed' hosts. By default, all compute nodes are
	'managed' nodes. To determine if a host is managed, execute:
	'rocks list host attr hostname | grep managed'. If you see output like:
	'compute-0-0: managed true', then the host is managed.
	</arg>

	<arg type='string' name='command'>
	The command to run on the list of hosts.
	</arg>

	<param type='boolean' name='managed'>
	Run the command only on 'managed' hosts, that is, hosts that generally
	have an ssh login. Default is 'yes'.
	</param>

	<param type='boolean' name='x11'>
	If 'no', disable X11 forwarding when connecting to hosts.
	Default is 'yes'.
	</param>

	<param type='string' name='timeout'>
	Sets the maximum length of time (in seconds) that the command is
	allowed to run.
	Default is '30'.
	</param>

	<param type='string' name='delay'>
	Sets the time (in seconds) to delay between each executed command
	on multiple hosts. For example, if the command is run on two
	hosts and if the delay is 10, then the command will be executed on host
	1, then 10 seconds later, the command will be executed on host 2.
	Default is '0' (no delay).
	</param>

	<param type='string' name='stats'>
	Display performance statistics if this parameter is set to 'yes'.
	Default is 'no'.
	</param>

	<param type='string' name='collate'>
	Prepend the hostname to every output line if this parameter is set to
	'yes'.
	Default is 'no'.
	</param>

	<param type='string' name='num-threads'>
	The number of threads to start in parallel. If num-threads is 0, then
	try to run the command in parallel on all hosts. Default is '128'.
	</param>

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

	def nodeup(self, hostif):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(2.0)
		try:
			#
			# this catches the case when the host is down
			# and/or there is no ssh daemon running
			#
			sock.connect((hostif, 22))

			#
			# this catches the case when the node is up,
			# sshd is sitting on port 22, but it is not
			# responding (e.g., the node is overloaded,
			# sshd is hung, etc.)
			#
			# sock.recv() should return something like:
			#
			#	SSH-2.0-OpenSSH_4.3
			#
			buf = sock.recv(64)
			#
			# this sends an SSH identification string to
			# the node; if not sent, the node will log
			# that an identification string was never
			# received (which may trigger an IDS)
			#
			sock.send('SSH-2.0-nodeup\r\n')
			#
			# this receives a string of key exchange (kex)
			# algorithms from the node; if not received
			# and the connection is severed, the node will
			# log a fatal error.
			#
			buf = sock.recv(1024)
			sock.close()
		except:
			return 0

		return 1


	def run(self, params, args):
		(args, command) = self.fillPositionalArgs(('command', ))

		if not command:
			self.abort('must supply a command')

		(managed, x11, t, d, s, c, n) = \
			self.fillParams([
				('managed', 'y'),
				('x11', 'y'),
				('timeout', '30'),
				('delay', '0'),
				('stats', 'n'),
				('collate', 'n'),
				('num-threads', '128')
			])

		try:
			timeout = int(t)
		except:
			self.abort('"timeout" must be an integer')

		if timeout < 0:
			self.abort('"timeout" must be a postive integer')

		try:
			numthreads = int(n)
		except:
			self.abort('"num-threads" must be an integer')

		try:
			delay = float(d)
		except:
			self.abort('"delay" must be a floating point number')

		hosts = self.getHostnames(args, self.str2bool(managed))
		
		# This is the same as doing -x using ssh.  Might be useful
		# for the common case, but required for the Viz Roll.

		if not self.str2bool(x11):
			try:
				del os.environ['DISPLAY']
			except KeyError:
				pass

		collate = self.str2bool(c)
		stats = self.str2bool(s)

		if collate:
			self.beginOutput()

		if numthreads <= 0:
			numthreads = len(hosts)

		threads = []

		i = 0
		work = len(hosts)
		while work:
			localhost = socket.gethostname().split('.')[0]
			while i < numthreads and i < len(hosts):
				host = hosts[i]
				# Is this host me?
				runlocal = (localhost == host.split('.')[0])
				i += 1	

				try:
					hnet=self.db.getHostAttr(host,'primary_net')
					query="select net.ip from networks net, nodes n, subnets s where net.node=n.id and net.subnet=s.id and n.name='%s' and s.name='%s'" % (host,hnet)
					self.db.execute(query)
					hostif,=self.db.fetchone()
				except:
					hostif=host
				#
				# first test if the node is up and responding
				# to ssh
				#
				if not runlocal and not self.nodeup(hostif):
					if collate:
						self.addOutput(host, 'down')
					else:
						print '%s: down' % host

					numthreads += 1
					work -= 1
					continue

				#
				# fire off the command
				#
				if runlocal:
					cmd = ('bash', '-c', command)
				else:
					cmd = ('ssh', hostif, command)

				p = Parallel(self, cmd, host, hostif, stats, collate)
				p.start()
				threads.append(p)

				if delay > 0:
					time.sleep(delay)

			#
			# collect completed threads
			#
			try:
				totaltime = time.time()
				while timeout == 0 or \
					(time.time() - totaltime) < timeout:

					active = threading.enumerate()

					t = threads
					for thread in t:
						if thread not in active:
							thread.join(0.1)
							threads.remove(thread)
							numthreads += 1
							work -= 1

					if len(active) == 1:
						break
				
					#
					# don't burn a CPU while waiting for the
					# threads to complete
					#
					time.sleep(0.5)

			except KeyboardInterrupt:
				#
				# try to collect all the active threads
				#
				active = threading.enumerate()

				t = threads
				for thread in t:
					if thread not in active:
						thread.join(0.1)
						threads.remove(thread)

				#
				# no more work to do if the user hits
				# control-c
				#
				work = 0

		#
		# kill all still active threads
		#
		active = threading.enumerate()
		if len(active) >= 2:
			for i in range(1, len(active)):
				active[i].kill()

		if collate:
			self.endOutput(padChar='')

RollName = "base"
