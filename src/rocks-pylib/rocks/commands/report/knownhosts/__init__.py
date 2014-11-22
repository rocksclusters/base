#$Id: __init__.py,v 1.7 2013/02/13 23:16:51 clem Exp $
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
#  Create shosts.equiv file for host-based ssh authentication
#  starting from a copy of rocks report host
#  <roy.dragseth@uit.no>

import rocks.commands
import rocks.ip
import os.path
import subprocess

class command(rocks.commands.HostArgumentProcessor,
		rocks.commands.report.command):
	pass

class Command(command):
	"""
	Report the host to known hosts (public keys) for  
	/etc/ssh/ssh_known_hosts

	<example cmd='report knownhosts'>
	Outputs lists of public IPs to be used for /etc/ssh/ssh_known_hosts
	</example>
	"""
      
	def run(self, param, args):
		self.beginOutput()
		self.addOutput('localhost', '<file name="/etc/ssh/ssh_known_hosts">')
		self.addOutput('localhost', '# Added by rocks report knownhosts  #')
		self.addOutput('localhost', '#        DO NOT MODIFY              #')
		self.addOutput('localhost', '# If you need to add entries use    #')
		self.addOutput('localhost', '# /etc/ssh/ssh_known_hosts.local    #')


		# grab per-node public keys
		allhosts = {}
		cmd = """SELECT n.name, s.value FROM nodes n INNER JOIN
			 sec_node_attributes s ON s.node = n.id WHERE
			 s.attr = 'ssh_host_rsa_key.pub';"""
		self.db.execute(cmd)

		for (host,pubkey) in self.db.fetchall():
			allhosts[host] = pubkey.rstrip('\n')

		# now find all interfaces for this node with labeled 
		# dnszones. put an entry for each interface
		cmd = """SELECT n.name,s.dnszone,net.name,s.name FROM nodes n INNER JOIN
			 networks net ON net.node = n.id INNER JOIN 
			 subnets s on net.subnet = s.id; """
		self.db.execute(cmd)
		for (host,zone,ifname,subnet) in self.db.fetchall():
			if host in allhosts and zone is not None:
				if ifname is not None:
					hostname = ifname 
				else:
					hostname = host
				self.addOutput('localhost', 
					'%s.%s %s' % (hostname, zone, allhosts[host]))
				if subnet == 'private':
					self.addOutput('localhost', 
					 '%s %s' % (hostname, allhosts[host]))
					

		# now the cluster-wide public key
		cmd = """SELECT s.value FROM sec_global_attributes s 
			WHERE s.attr = 'ssh_host_rsa_key.pub';"""
		row = self.db.execute(cmd)
		if row > 0: 
			pubkey, = self.db.fetchone()
		else:
			pubkey = None
		if pubkey is not None:
			pubkey = pubkey.rstrip('\n')

		cmd = """SELECT dnszone FROM subnets where dnszone 
				IS NOT NULL AND subnets.name != 'public';"""
		self.db.execute(cmd)

		for zone, in self.db.fetchall():
			if pubkey is not None:
				self.addOutput('localhost', 
					'*.%s %s' % (zone,pubkey))

		# finally add the short names of all hosts
		cmd = """SELECT n.name,s.dnszone,net.name FROM nodes n INNER JOIN
			 networks net ON net.node = n.id INNER JOIN 
			 subnets s on net.subnet = s.id AND s.name = 'private'; """
		self.db.execute(cmd)

		if pubkey is not None:
			for (host,zone,ifname) in self.db.fetchall():
				if host not in allhosts:
					if ifname is not None:
						hostname = ifname 
					else:
						hostname = host
					self.addOutput('localhost', 
						'%s %s' % (hostname, pubkey))


		# Finally, add the ssh_known_hosts.local file to the list
		hostlocal = '/etc/ssh/ssh_known_hosts.local'
		try:
			f = open(hostlocal,'r')
			self.addOutput('localhost','#\n# Imported from %s\n#' % hostlocal)
			h = f.read()
			self.addOutput('localhost',h)
			f.close()
		except :
			pass


		self.addOutput('localhost', '</file>')
		self.endOutput(padChar='')


RollName = "base"
