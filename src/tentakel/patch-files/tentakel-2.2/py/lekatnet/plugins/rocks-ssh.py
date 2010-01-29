# $Id: rocks-ssh.py,v 1.6 2010/01/29 19:55:27 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# Copyright (c) 2002, 2003, 2004 Sebastian Stark
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR SEBASTIAN STARK
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# $Log: rocks-ssh.py,v $
# Revision 1.6  2010/01/29 19:55:27  bruno
# it is not enough to just check if a process has port 22 open on a node, we
# must also see if sshd is responding. we do that by trying to recv the
# ssh banner after connecting to port 22.
#
# Revision 1.5  2009/10/07 18:13:36  bruno
# make tentakel more resilient to hanging nodes. thanks to Roy Dragseth for
# the fix.
#
# Revision 1.4  2009/05/01 19:07:10  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 22:44:44  bruno
# moved tentakel from the hpc to the base roll
#
# Revision 1.6  2007/06/23 04:03:45  mjk
# mars hill copyright
#
# Revision 1.5  2006/09/11 22:48:55  mjk
# monkey face copyright
#
# Revision 1.4  2006/08/10 00:11:00  mjk
# 4.2 copyright
#
# Revision 1.3  2005/12/30 16:19:24  mjk
# - Removed ping test from contructor
# - Added socket test as suggested by Sebastian Stark
# - Tentakel now behaves like cluster-fork
#
# Revision 1.2  2005/12/30 05:58:30  mjk
# added insert-ethers plugin
#
# Revision 1.1  2005/12/29 23:21:56  mjk
# possible cluster-fork replacement
#


from lekatnet.remote import registerRemoteCommandPlugin
from lekatnet.remote import RemoteCommand
import time
import commands
import socket
import os
import re
import pexpect

# The RocksSSH method ("rocks") is identical to the default SSHMethod
# but we probe the machines with ping first to make sure they are online.
# This addition makes tentakel act more like cluster-fork.

class RocksSSHRemoteCommand(RemoteCommand):
	"Rocks SSH remote execution class"

	def __init__(self, destination, params):
		self.sshpath = params['ssh_path']
		self.user = params['user']
		RemoteCommand.__init__(self, destination, params)

	def _rexec(self, command):

		t1 = time.time()

		# The follow test was suggested by Sebastian Stark and
		# replaces our ping test of the machines.

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(2)
		try:
			#
			# this catches the case when the host is down and/or
			# there is no ssh daemon running
			#
			sock.connect((self.destination, 22))

			#
			# this catches the case when the node is up, sshd
			# is sitting on port 22, but it is not responding
			# (e.g., the node is overloaded, sshd is hung, etc.)
			#
			# sock.recv() should return something like:
			#
			#	SSH-2.0-OpenSSH_4.3
			#
			buf = sock.recv(64)
		except socket.error:
			self.duration = time.time() - t1
			return (-1, 'down')

		# SSH to the machine, this is the same code from the
		# stock SSHRemoteCommand class.

		s = '%s %s@%s "%s"' % (self.sshpath, self.user,
			self.destination, command)
		try:
			p = pexpect.spawn(s)
			p.expect(pexpect.EOF)
			output = p.before
			status = 0
		except pexpect.TIMEOUT, e:
			output = "Remote command timed out on host %s" % \
				self.destination
			status = 1

		p.close()

		self.duration = time.time() - t1
		return (status >> 8, output)


registerRemoteCommandPlugin('rocks', RocksSSHRemoteCommand)

