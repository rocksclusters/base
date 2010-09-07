# $Id: __init__.py,v 1.2 2010/09/07 23:53:00 bruno Exp $
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
# Revision 1.2  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.1  2010/06/30 17:37:33  anoop
# Overhaul of the naming system. We now support
# 1. Multiple zone/domains
# 2. Serving DNS for multiple domains
# 3. No FQDN support for network names
#    - FQDN must be split into name & domain.
#    - Each piece information will go to a
#      different table
# Hopefully, I've covered the basics, and not broken
# anything major
#
# Revision 1.5  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.4  2009/03/04 21:16:54  bruno
# replace getGlobalVar with getHostAttr
#
# Revision 1.3  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.1  2007/08/08 22:14:41  bruno
# moved 'dbreport named' and 'dbreport dns' to rocks command line
#
#

import os
import string
import rocks.commands

config_preamble = """options {
	directory "/var/named";
	dump-file "/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	forwarders { %s; };
};

controls {
	inet 127.0.0.1 allow { localhost; } keys { rndckey; };
};

zone "." IN {
	type hint;
	file "named.ca";
};

zone "localdomain" IN {
	type master;
	file "localdomain.zone";
	allow-update { none; };
};

zone "localhost" IN {
	type master;
	file "localhost.zone";
	allow-update { none; };
};

zone "0.0.127.in-addr.arpa" IN {
	type master;
	file "named.local";
	allow-update { none; };
};

zone "0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
	type master;
	file "named.ip6.local";
	allow-update { none; };
};

zone "255.in-addr.arpa" IN {
	type master;
	file "named.broadcast";
	allow-update { none; };
};

zone "0.in-addr.arpa" IN {
	type master;
	file "named.zero";
	allow-update { none; };
};
"""

zone_template = """
zone "%s" {
	type master;
	notify no;
	file "%s.domain";
};

zone "%s.in-addr.arpa" {
	type master;
	notify no;
	file "reverse.%s.domain.%s";
};
"""

class Command(rocks.commands.report.command):
	"""
	Prints the nameserver daemon configuration file
	for the system.

	<example cmd="report named">
	Outputs /etc/named.conf
	</example>
	"""

	def run(self, params, args):
		
		# Start writing the named.conf file
		s = '<file name="/etc/named.conf" perms="0644">\n'

		# Get a list of all the Public DNS servers
		fwds = self.db.getHostAttr('localhost','Kickstart_PublicDNSServers')
		forwarders = string.join(fwds.split(','), ';')
		
		# Create the preamble from the template
		s += config_preamble % (forwarders)

		# Get a list of all networks that we should serve
		# domain names for
		for n in self.getNetworks():
			# For every network, get the base subnet,
			# and reverse it. This is basically the
			# format that named understands
			sn	= self.getSubnet(n.subnet, n.netmask)
			sn.reverse()
			r_sn	= string.join(sn, '.')
			
			# Add the zone to the named.conf file
			s += zone_template % (n.dnszone, n.name, \
					r_sn, n.name, r_sn)
		
		# Check if there are local modifications to named.conf
		if os.path.exists('/etc/named.conf.local'):
			f = open('/etc/named.conf.local', 'r')
			s += f.read()
			f.close()
			s += '\n'
			
		s += 'include "/etc/rndc.key";\n'
		s += '</file>\n'

		self.beginOutput()
		self.addOutput('localhost',s)
		self.endOutput(padChar = '')
