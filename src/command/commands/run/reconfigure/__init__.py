# $Id: __init__.py,v 1.12 2012/11/27 00:48:26 phil Exp $
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

import os
import string
import rocks.gen
import rocks.commands
import rocks.commands.set.attr
import rocks.commands.run
import tempfile
import IPy
from socket import inet_ntoa
from struct import pack


class Command(rocks.commands.run.command):
	"""
	Generates a script which can be used to reconfigure a system after 
	some attributes have been changed.
	
	<param type='boolean' name='clear'>
	If clear is true the command will remove all the _old attributes from the database.
	This command should be run at the beginning of a reconfigure session.
	Default is 'no'.
	</param>

	<param type='boolean' name='showattr'>
	When true it prints the attributes that will be changed when running reconfigure.
	For example if the user changes the Kickstart_PublicAddress attribute reconfigure will 
	update the Kickstart_PublicBroadcast and Kickstart_PublicNetwork attributes accordingly.
	This flag can be used to verify what reconfigure will change.

	Reconfigure will change only the attributes named Kickstart_Private*/Kickstart_Public*
	Default is 'no'.
	</param>

	<arg optional='1' type='string' name='roll' repeat='1'>
	Not implemented. This argument is not implemented
	</arg>

	<example cmd='run reconfigure'>
	Generate a script to reconfigure the current system
	</example>
	"""

	def run(self, params, args):

		(clear, showattr) = \
			self.fillParams([
				('clear', 'n'),
				('showattr', 'n')
			])

		hostname = 'localhost'

		#
		# show which attr will be modified
		#
		if self.str2bool(showattr) :
			current_attr = self.db.getHostAttrs(hostname)
			attrs = self.get_modified_attr(hostname, current_attr)
			additional_attr = get_additional_attr(attrs, current_attr)

			self.addText("User modified attributes\n")
			self.beginOutput()
			for name in attrs:
				self.addOutput("", (name, current_attr[name + "_old"], attrs[name]))
			
			if additional_attr :
				self.addOutput("", (" ", " ", " "))
				self.addOutput("", ("Additional attributes", " ", " "))
				for name in additional_attr:
					self.addOutput("", (name, current_attr[name], additional_attr[name]))
			self.endOutput(header=['host', 'attr', 'old value ->', 'new value'])
			return

		#
		# clear attributes historical values
		#
		if self.str2bool(clear) :
			current_attr = self.db.getHostAttrs(hostname, 1)
			for name in current_attr:
				if name.endswith("_old"):
					# we need to delete this one
					if current_attr[name][1] == 'H':
						command = 'remove.host.attr'
					elif current_attr[name][1] == 'G':
						command = 'remove.attr'
					elif current_attr[name][1] == 'A':
						command = 'remove.appliance.attr'
					elif current_attr[name][1] == 'O':
						command = 'remove.os.attr'
					self.command(command, [name])
			return

		#
		# really run the script
		#

		# first fix the missing attribute
		current_attr = self.db.getHostAttrs(hostname)
		attrs = self.get_modified_attr(hostname, current_attr)
		additional_attr = get_additional_attr(attrs, current_attr)
		for name in additional_attr:
			if name == 'dhcp_nextserver':
				# this is an appliance attribute it needs special care
				rows = self.db.execute('''select name
					from appliance_attributes, appliances
					where Appliance = id and
					Attr = "dhcp_nextserver"''')
				for app_name, in self.db.fetchall():
					self.command('set.appliance.attr',
						[app_name, name, additional_attr[name]])
			else:
				self.command('set.attr', [name, additional_attr[name]])


		rolls = []
		for roll in args:
			rolls.append(roll)
		xml = self.command('list.host.xml', [ hostname,
			'roll=%s' % string.join(rolls, ',') ])


		if self.os != 'linux':
			self.abort('it runs only on linux!!')
		gen = rocks.gen.Generator_linux()
		# set reconfigure stage
		gen.set_phases(["reconfigure"])
		gen.parse(xml)

		script = []
		script.append('#!/bin/sh\n')
		script += gen.generate_config_script()
		self.addText(string.join(script, ''))


	def get_modified_attr(self, hostname, current_attrs):
		"""it returns a dictionary of the attributes with _old values"""
		ret_dict = {}
		for name in current_attrs:
			if name.endswith(rocks.commands.set.attr.postfix):
				real_name = name[:-len(rocks.commands.set.attr.postfix)]
				ret_dict[real_name] = current_attrs[real_name]
		return ret_dict



def get_additional_attr(changed_attrs, current_attrs):
	""" given the attribute changed by the user it returns a dictionary with
	the set of attributes that should be changed.

	# run a doctest to verify it does what I want
	>>> result =  get_additional_attr({'Kickstart_PublicHostname': 'somenew.hostname.edu', \
		'Kickstart_PublicAddress': '123.1.2.3', 'Kickstart_PrivateAddress' : '10.4.2.1'},\
		 {"Kickstart_PublicNetmask": "255.255.255.0", "Kickstart_PrivateNetmask": "255.255.0.0"})
	>>> result # doctest: +ELLIPSIS
	{...}
	>>> result == \
		{'Kickstart_PrivateHostname': 'somenew', 'Kickstart_PublicNetmask': '123.1.2.0', \
		'Kickstart_PublicBroadcast': '123.1.2.255', 'Kickstart_PublicDNSDomain': 'hostname.edu', \
		'Kickstart_PrivateNetmask': '10.4.0.0', 'Kickstart_PrivateBroadcast': '10.4.255.255', \
		'Kickstart_PrivateGateway': '10.4.2.1', 'Kickstart_PrivateKickstartHost': '10.4.2.1', \
		'dhcp_nextserver': '10.4.2.1', 'Kickstart_PrivateDNSServers': '10.4.2.1', \
		'Kickstart_PrivateNTPHost': '10.4.2.1', 'Kickstart_PrivateSyslogHost': '10.4.2.1'}
	True
	"""
	fix_functions = [_fix_fqdn, _fix_networks]
	return_dict = {}

	# for each changed attribute we call the fix functions
	for name, value in changed_attrs.iteritems():
		for function in fix_functions:
			new_values = function(name, value, current_attrs, changed_attrs)
			for new_name, new_value in new_values.iteritems():
				_check_new_value(return_dict, new_name, new_value)
				if _check_new_value(changed_attrs, new_name, new_value):
					return_dict[new_name] = new_values[new_name]
	return return_dict


def _fix_fqdn(name, value, current_attrs, changed_attrs):
	"""handle changes to the FQDN whcih means the attributes:
	Kickstart_PublicHostname   -> fqdn
	Kickstart_PublicDNSDomain  -> domainname
	Kickstart_PrivateHostname  -> hostname
	
	Info_ClusterName is not linked with those attribute """
	ret_dict = {}
	if name == "Kickstart_PublicHostname":
		ret_dict['Kickstart_PublicDNSDomain'] = value[value.find('.') + 1:]
		ret_dict['Kickstart_PrivateHostname'] = value.split('.')[0]
	elif name == "Kickstart_PublicDNSDomain":
		hostname = current_attrs['Kickstart_PublicHostname'].split('.')[0]
		ret_dict['Kickstart_PublicHostname'] = hostname + '.' + value
	elif name == "Kickstart_PrivateHostname":
		fqdn = current_attrs['Kickstart_PublicHostname']
		domainname = fqdn[fqdn.find('.'):]
		ret_dict['Kickstart_PublicHostname'] = value + domainname
	return ret_dict


def _fix_networks(name, value, current_attrs, changed_attrs):
	"""handle the change to the IP address attributes (public and private)
	It touches the following attrs:
	Kickstart_PublicAddress Kickstart_PrivateAddress
	Kickstart_PublicBroadcast Kickstart_PrivateBroadcast
	Kickstart_PublicNetmaskCIDR Kickstart_PrivateNetmaskCIDR
	Kickstart_PublicNetwork Kickstart_PrivateNetwork
	Kickstart_PublicNetmask Kickstart_PrivateNetmask
	"""
	if name.startswith("Kickstart_Public"):
		type = "Public"
	elif name.startswith("Kickstart_Private"):
		type = "Private"
	else:
		return {}

	kickstart_address = "Kickstart_%sAddress" % type
	kickstart_broadcast = "Kickstart_%sBroadcast" % type
	kickstart_network = "Kickstart_%sNetwork" % type
	kickstart_netmask_cidr = "Kickstart_%sNetmaskCIDR" % type
	kickstart_netmask = "Kickstart_%sNetmask" % type
	
	ret_dict={}
	change_broadcast = False
	if name == kickstart_address:
		change_broadcast = True
		if type == "Private":
			ret_dict['Kickstart_PrivateDNSServers'] = value
			ret_dict['Kickstart_PrivateGateway'] = value
			ret_dict['Kickstart_PrivateKickstartHost'] = value
			ret_dict['Kickstart_PrivateNTPHost'] = value
			ret_dict['Kickstart_PrivateSyslogHost'] = value
			ret_dict['dhcp_nextserver'] = value
			ret_dict['Kickstart_PrivateSyslogHost'] = value
	elif name == kickstart_broadcast:
		# we do nothing in this case
		pass
	elif name == kickstart_netmask_cidr:
		ret_dict[kickstart_netmask] = _get_netmask_from_CIDR(value)
		change_broadcast = True
	elif name == kickstart_network:
		pass
	elif name == kickstart_netmask:
		ret_dict[kickstart_netmask_cidr]  = _get_CIDR_from_netmask(value)
		change_broadcast = True
	if change_broadcast :
		# recalculate broadcast
		if kickstart_address in changed_attrs:
			ip_addr = changed_attrs[kickstart_address]
		else:
			ip_addr = current_attrs[kickstart_address]
		if kickstart_netmask_cidr in changed_attrs:
			netmask = _get_netmask_from_CIDR(
				changed_attrs[kickstart_netmask_cidr])
		elif kickstart_netmask in changed_attrs:
			netmask = changed_attrs[kickstart_netmask]
		else:
			netmask = current_attrs[kickstart_netmask]
		ip_temp =  IPy.IP(value + '/' + netmask, make_net=True)
		ret_dict[kickstart_network] = str(ip_temp.net())
		ret_dict[kickstart_broadcast] = str(ip_temp.broadcast())
	return ret_dict


def _check_new_value(dictionary, new_name, new_value):
	"""verify that if new_name exists in dictionary its value is equal to new_value"""
	if new_name not in dictionary :
		return True
	elif dictionary[new_name] != new_value :
		msg = 'There is a confict with the attribute ' + new_name
		msg += ' the values ' + new_value + ' and ' + dictionary[new_name]
		msg += ' conflict'
		rocks.commands.Abort(msg)
	return False

def _get_CIDR_from_netmask(netmask):
	"""return the cidr string of the given netmask"""
	return str(sum([bin(int(x)).count('1') for x in netmask.split('.')]))

def _get_netmask_from_CIDR(cidr):
	mask = int(cidr)
	bits = 0xffffffff ^ (1 << 32 - mask) - 1
	return inet_ntoa(pack('>I', bits))



if __name__ == '__main__':
    import doctest
    doctest.testmod()
