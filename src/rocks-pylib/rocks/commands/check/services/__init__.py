#!/opt/rocks/bin/python
# 
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
#
#
#

import socket
import shlex

import rocks.commands
import subprocess

class Command(rocks.commands.Command):
	"""
	Checks that all Rocks required services are up and running, If a
	required services is not running it will reported.
	
	<example cmd='check host services'>
	Check that all required services are up and running.
	</example>
	"""

	def checkService(self, cmdname, error_msg):
		"""check if the given cmdname returns 0 once executed.
		If cmdname fails it returns  runninvg"""
		devnull = open('/dev/null', 'w')
		process = subprocess.Popen(shlex.split(cmdname), stdout=devnull, stderr=devnull)
		retcode = process.wait()
		devnull.close()
		if retcode != 0:
			self.abort(error_msg)

	def run(self, params, args):

		if len(args) != 0:
			self.abort("check services does not accept any argument")

		if socket.gethostname().split('.')[0] != self.newdb.getFrontendName():
			self.abort('this command should run only on the frontend')


		# dhcpd
		cmd = "service dhcpd status"
		error_msg = "dhcpd is not running.\n" + \
			"Restart it with 'service dhcpd start'"
		self.checkService(cmd, error_msg)

		# xinetd
		cmd = "curl 'tftp://localhost/pxelinux.0' -o /dev/null"
		error_msg = "unable to download pxelinux with tftp.\n" + \
			"Verify that xinetd is running with 'service xinetd start'"
		self.checkService(cmd, error_msg)

		# httpd wget kickstart
		cmd = "bash -c \"curl -k 'https://localhost/install/sbin/kickstart.cgi?arch=x86_64&np=1' | xmllint -\""
		error_msg = "unable to download kickstart.\n" + \
			"Verify httpd is running with 'service httpd start'"
		self.checkService(cmd, error_msg)
		
		# sec channel
		cmd = "rpcinfo -T tcp localhost  536870913"
		error_msg = "sec_channel RPC is not available.\n" + \
			"Restart rpcbind with 'service rpcbind restart' and then " + \
			"restart 'service sec-channel restart' and n" + \
			"fs 'service nfs restart'"
		self.checkService(cmd, error_msg)
		cmd = "rpcinfo -T udp localhost  536870913"
		self.checkService(cmd, error_msg)

		return True


RollName = "kvm"
