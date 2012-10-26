# $Id: plugin_hostauth.py,v 1.6 2012/10/26 22:48:33 clem Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
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
# $Log: plugin_hostauth.py,v $
# Revision 1.6  2012/10/26 22:48:33  clem
# need to use full path to /opt/rocks/bin/rocks
#
# If not during the installation when rocks sync config in an init script
# it fails because it does not find rocks
#
# Revision 1.5  2012/10/04 21:55:01  phil
# sync only to self and to subordinate login appliances. Generic frontends was too expansive as it included virtual frontends too.
#
# Revision 1.4  2012/08/14 17:29:30  phil
# with hostbased authentication, remove /etc/ssh/rocks_autogen_user_keys on frontend
# and login appliances
#
# Revision 1.3  2012/08/14 04:51:45  phil
# Generate ssh_known_hosts file.
# Works when hosts are multi-homed (like Triton)
#
# Revision 1.2  2012/08/13 05:12:17  phil
# Hostbased Authentication now default method. Thanks, Roy Dragseth.
#
#

import rocks.commands
import subprocess

class Plugin(rocks.commands.Plugin):
	def provides(self):
		return 'hostauth'
		
	def run(self, args):
		""" if rocks_autogen_user_keys is true, then touch 
		    file. Else remove it. Works with /etc/profile.d/ssh-key.sh.
		    Always regenerates /etc/ssh/shosts.equiv
		"""		
		touchfile = '/etc/ssh/rocks_autogen_user_keys'
		autogen = self.db.getHostAttr('localhost',
				'rocks_autogen_user_keys')
		try:
			if (autogen.lower() == 'true' ):
				subprocess.call("/opt/rocks/bin/rocks run host localhost login '/bin/touch %s'" % touchfile, shell=True)
			else:
				subprocess.call("/opt/rocks/bin/rocks run host localhost login '[ -f %s ] && /bin/rm %s'" 
						% (touchfile,touchfile), shell=True)
		except:
			subprocess.call("/opt/rocks/bin/rocks run host localhost login '[ -f %s ] && /bin/rm %s'" 
						% (touchfile,touchfile), shell=True)

		# regenerate shosts and publish via 411
		p = subprocess.call("/opt/rocks/bin/rocks report shosts | /opt/rocks/bin/rocks report script | sh > /dev/null 2>&1", 
			shell=True) 
		p = subprocess.call("/opt/rocks/bin/rocks report knownhosts | /opt/rocks/bin/rocks report script | sh > /dev/null 2>&1", 
			shell=True) 
		p = subprocess.call("make -C /var/411 > /dev/null 2>&1", 
			shell=True) 
