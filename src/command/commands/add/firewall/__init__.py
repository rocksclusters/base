# $Id: __init__.py,v 1.8 2011/05/28 03:25:26 phil Exp $RAM
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.8  2011/05/28 03:25:26  phil
# Add Firewall, report firewall now working with resolved rules.
# Created a TEMPTABLES database for temporary SQL tables.
# Still needs full testing.
#
# Revision 1.7  2011/05/27 19:06:48  phil
# First edition of new firewall add rule.
# Still needs error handling/checking.
#
# Revision 1.6  2011/02/24 20:10:28  bruno
# Added documentation and examples to the add/close/open firewall commands.
# Thanks to Larry Baker for the suggestion.
#
# Revision 1.5  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.4  2010/05/11 22:28:15  bruno
# more tweaks
#
# Revision 1.3  2010/05/07 23:13:32  bruno
# clean up the help info for the firewall commands
#
# Revision 1.2  2010/05/04 22:04:14  bruno
# more firewall commands
#
# Revision 1.1  2010/04/30 22:07:16  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#

import string
import rocks.commands

class command(rocks.commands.CategoryArgumentProcessor, rocks.commands.add.command):
	def serviceCheck(self, service):
		#
		# a service can look like:
		#
		#	reserved words: all, nat
		#       named service: ssh
		#       specific port: 8069
		#       port range: 0:1024
		#
		if service in [ 'all', 'nat' ]:
			#
			# valid
			#
			return

		if service[0] in string.digits:
			#
			# if the first character is a number, then assume
			# this is a port or port range:
			#
			ports = service.split(':')
			if len(ports) > 2:
				msg = 'port range "%s" is invalid. ' % service
				msg += 'it must be "integer:integer"'
				self.abort(msg)

			for a in ports:
				try:
					i = int(a)
				except:
					msg = 'port specification "%s" ' % \
						service
					msg += 'is invalid. '
					msg += 'it must be "integer" or '
					msg += '"integer:integer"'
					self.abort(msg)

		#
		# if we made it here, then the service definition looks good
		#
		return


	def checkArgs(self, service, network, outnetwork, chain, action,
		protocol, flags, comment):

		if not service:
			self.abort('service required')
		if not network and not outnetwork:
			self.abort('network or output-network required')
		if not chain:
			self.abort('chain required')
		if not action:
			self.abort('action required')
		if not protocol:
			self.abort('protocol required')

		#
		# check if the network exists
		#
		if network == 'all':
			network = 0
		elif network:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % (network))

			if rows == 0:
				self.abort('network "%s" not in the database. Run "rocks list network" to get a list of valid networks.' % network)

			network, = self.db.fetchone()
		else:
			network = 'NULL'

		if outnetwork == 'all':
			outnetwork = 0
		elif outnetwork:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % (outnetwork))

			if rows == 0:
				self.abort('output-network "%s" not in the database. Run "rocks list network" to get a list of valid networks.')

			outnetwork, = self.db.fetchone()
		else:
			outnetwork = 'NULL'

		self.serviceCheck(service)

		action = action.upper()
		chain = chain.upper()

		if protocol:
			protocol = '"%s"' % protocol
		else:
			protocol = 'NULL'

		if flags:
			flags = '"%s"' % flags
		else:
			flags = 'NULL'

		if comment:
			comment = '"%s"' % comment
		else:
			comment = 'NULL'

		return (service, network, outnetwork, chain, action,
			protocol, flags, comment)


	def insertRule(self, category, index, rulename,  
		service, network, outnetwork, chain, action, protocol, 
		flags, comment):

		#
		# all input has been verified. add the row
		#
		try: 
			self.db.execute("""INSERT INTO firewalls 
				(category, catindex, 
				rulename, insubnet, outsubnet, service, 
				protocol, action, chain, flags, 
				comment) 
				VALUES (mapCategory('%s'), mapCategoryIndex('%s','%s'), 
				'%s', %s, %s, '%s', 
	                        %s, '%s', '%s', %s,
	                        %s )""" %
				(category, category, index, 
				rulename, network, outnetwork, service, 
				protocol, action, chain, flags, 
				comment))
		except:
			print "Rule '%s' already exists for %s=%s" % (rulename,category,index)


class Command(command):
	"""
	Add a firewall rule to the a category in cluster.

	<arg type='string' name='category=index'>
	[global,os,appliance,host]=index.

	Must precede all other a=b parameters

        Apply rule to index (member) of category. e.g.
	os=linux, appliance=login, or host=compute-0-0.

        global, global=, and global=global all refer
        to the global category
	</arg>

	<param type='string' name='rulename' optional='1'>
	User-defined name of rule. If omitted, defined as 
        CHAIN&lt;NN&gt; where NN is
        arbitrary. Firewall rules are ordered lexicographically. 
	</param>

	<param type='string' name='service'>
	The service identifier, port number or port range. For example
	"www", 8080 or 0:1024.
	To have this firewall rule apply to all services, specify the
	keyword 'all'.
	</param>

	<param type='string' name='protocol'>
	The protocol associated with the rule. For example, "tcp" or "udp".
	To have this firewall rule apply to all protocols, specify the
	keyword 'all'.
	</param>
	
        <param type='string' name='network'>
        The network this rule should be applied to. This is a named network
        (e.g., 'private') and must be one listed by the command
        'rocks list network'.
	To have this firewall rule apply to all networks, specify the
	keyword 'all'.
	</param>

        <param type='string' name='output-network' optional='1'>
        The output network this rule should be applied to. This is a named
	network (e.g., 'private') and must be one listed by the command
        'rocks list network'.
	</param>

        <param type='string' name='chain'>
	The iptables 'chain' this rule should be applied to (e.g.,
	INPUT, OUTPUT, FORWARD).
	</param>

        <param type='string' name='action'>
	The iptables 'action' this rule should be applied to (e.g.,
	ACCEPT, REJECT, DROP).
	</param>

	<example cmd='add firewall appliance=login rulename=ACCEPT-SSH network=public service="ssh" protocol="tcp" action="ACCEPT" chain="INPUT" flags="-m state --state NEW"'>
	Accept TCP packets for the ssh service on the public network on
	the INPUT chain and apply the "-m state --state NEW" flags to the
	rule.
        
        Apply the rule to login appliances (appliance=login)

	Name the rule ACCEPT-SSH

	If 'eth1' is associated with the public network, this will be
	translated as the following iptables rule:
	"-A INPUT -i eth1 -p tcp --dport ssh -m state --state NEW -j ACCEPT"
	</example>

	<example cmd='add firewall global rulename=ACCEPT-PRIVATE network=private service="all" protocol="all" action="ACCEPT" chain="INPUT"'>
	Accept all protocols and all services on the private network on the
	INPUT chain.

	Apply this rule to all nodes in the cluster (global)

	If 'eth0' is the private network, then this will be translated as
	the following iptables rule:
	"-A INPUT -i eth0 -j ACCEPT"
	</example>


	<example cmd='add firewall host=compute-0-0 rulename=ZZDRACONIAN network="all" service="all" protocol="all" action="DROP" chain="INPUT"'>
        DROP all non-matched packets

	Apply this rule to host compute-0-0 (host=compute-0-0)

        rule will be named ZZDRACONIAN 

	This will drop all non-matched packets  that have not been previously accepted
        Known as a draconian firewall rule. 
	</example>
	"""
	def run(self, params, args):
		(rulename,service, network, outnetwork, chain, action, 
			protocol, flags, comment) = self.fillParams([
				('rulename',),
				('service', ),
				('network', ),
				('output-network', ),
				('chain', ),
				('action', ),
				('protocol', ),
				('flags', ),
				('comment', )
			])
		
		


		(service, network, outnetwork, chain, action, protocol, flags,
			comment) = self.checkArgs(service, network,
			outnetwork, chain, action, protocol, flags, comment)

		# Get (category,index) pairs that this rule affects.
		myargs = args[:]
		if params.has_key('@ROCKSPARAM0'):
			myargs.append(params['@ROCKSPARAM0'])

		indices =  self.getCategoryIndices(myargs)

		for category,index in indices:
			self.insertRule(category,index,rulename,service, 
				network, outnetwork, chain, action, protocol, flags, comment)

			
