# $Id: __init__.py,v 1.8 2012/11/27 00:48:31 phil Exp $

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

# $Log: __init__.py,v $
# Revision 1.8  2012/11/27 00:48:31  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.7  2012/08/10 18:55:48  phil
# Typo.
#
# Revision 1.6  2012/08/10 18:24:16  phil
# Add two imports
#
# Revision 1.5  2012/08/09 21:20:57  phil
# fix generation of cluster-wide ssh key
# when sync host sharekey runs, don't contaminate root's authorized_keys file
#
# Revision 1.4  2012/05/06 05:48:38  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:30:41  phil
# Viper Copyright
#
# Revision 1.2  2011/04/21 02:31:39  anoop
# sync commands now take advantage of new parallel class
#
# Revision 1.1  2011/04/14 23:08:59  anoop
# Move parallel class up one level, so that all sync commands can
# take advantage of it.
#
# Added rocks sync host sharedkey. This distributes the 411 shared key
# to compute nodes
#

import os
import tempfile
import rocks.commands
from rocks.commands.sync.host import Parallel
from rocks.commands.sync.host import timeout


class Command(rocks.commands.sync.host.command):
	"""This command syncs the shared 411 key 
	on a particular host"""

	def run(self, params, args):
		# Get hostnames from args
		hosts = self.getHostnames(args)

		fname = '/etc/411-security/shared.key'



		# create a known hosts temporary file
		# this is so we don't contaminate the regular known hosts file	
		# since this sync might change the host keys.
		(khfid, khfname) = tempfile.mkstemp()

		# Copy the 411 shared key to all nodes
		threads = []

		for host in hosts:
			cmd = 'scp -q -o UserKnownHostsFile=%s %s root@%s:%s' % \
				(khfname,fname, host, fname)
			p = Parallel(cmd, host)
			p.start()
			threads.append(p)

		for thread in threads:
			thread.join(timeout)

		if os.path.exists(khfname):
			os.unlink(khfname)
