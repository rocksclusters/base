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

import rocks.commands
import rocks.ip
import sqlalchemy
from rocks.db.mappings.base import *


class command(rocks.commands.HostArgumentProcessor,
		rocks.commands.report.command):
	pass

class Command(command):
	"""
	Report the next available IP address on the given subnet

	<arg type='string' name='subnet'>
	The subnet name that we should use
	</arg>

	<param type='int' name='increment'>
	The increment that should be used to find the next available IP
	Default to -1
        </param>

	<param type='string' name='baseip'>
	The starting IP address we should use to generate IPs
        </param>

	<example cmd='report nextip private'>
	Output the next available IP on the private subnet
	</example>
	"""
      


	def run(self, param, args):

		(increment, baseip) = self.fillParams( [
			('increment', '-1'), 
			('baseip', '')
			])

		if len(args) != 1:
			self.abort('must supply the subnet')

		increment = int(increment)

		subnet = args[0]
		
		try:			
			subnet_db = self.newdb.getSession().query(rocks.db.mappings.base.Subnet)\
				.options(sqlalchemy.orm.joinedload('networks'))\
				.filter(Subnet.name == subnet).one()
		except sqlalchemy.orm.exc.NoResultFound:
			self.abort('subnet %s is not valid' % subnet)

		mask_ip = rocks.ip.IPAddr(subnet_db.netmask)
		network_ip = rocks.ip.IPAddr(subnet_db.subnet)
		bcast_ip = rocks.ip.IPAddr(network_ip | rocks.ip.IPAddr(~mask_ip))
		bcast = "%s" % (bcast_ip)
		used_ip = [ net.ip for net in subnet_db.networks]
		
		# Create the IPGenerator and if the user choose a 
		# base ip address to the IPGenerator to start there.
		# Should really be a method in the class to set this,
		# but I need this today on 3.2.0.  Revisit soon (mjk)
		ip = rocks.ip.IPGenerator(bcast, subnet_db.netmask)
		if baseip:
			ip.addr = rocks.ip.IPAddr(baseip)

		#
		# look in the database for a free address
		#
		while 1:
		
			# Go to the next ip address.  Default is still
			# to count backwards, but allow the user to
			# set us to count forwards.
			nextip = ip.next(increment)
			if str(nextip) not in used_ip:
				# we found it
				break

		self.beginOutput()
		self.addOutput('localhost', nextip)
		self.endOutput(padChar='')


RollName = "base"
