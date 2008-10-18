# $Id: plugin_named.py,v 1.3 2008/10/18 00:55:58 mjk Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
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
# $Log: plugin_named.py,v $
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

config_template = """options {
	directory "/var/named";
	dump-file "/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	%s
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

zone "%s" {
	type master;
	notify no;
	file "rocks.domain";
};

%s
include "/etc/rndc.key";
"""

zone_template = """
zone "%s.in-addr.arpa" {
	type master;
	notify no;
	file "reverse.rocks.domain.%s";
};
"""

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'named'
		
	#def requires(self):
		#return ['dns']

	def run(self, args):
		domain = self.db.getGlobalVar('Kickstart', 'PrivateDNSDomain')
		nameservers = self.db.getGlobalVar('Kickstart',
			'PublicDNSServers')

		file = open('/etc/named.conf', 'w')

		ns = ''
		if len(string.strip(nameservers)) > 0:
			ns = 'forwarders { %s; };' % \
				string.join(string.split(nameservers, ','), ';')

		zone = ''
		for subnet in self.owner.getSubnets():
			subnet.reverse()
			zonename = string.join(subnet, '.')

			zone += zone_template % (zonename, zonename)

		file.write(config_template % (ns, domain, zone))
		file.close()

