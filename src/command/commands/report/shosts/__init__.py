# $Id: __init__.py,v 1.3 2012/11/27 00:48:25 phil Exp $
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
#  Create shosts.equiv file for host-based ssh authentication
#  starting from a copy of rocks report host
#  <roy.dragseth@uit.no>

import rocks.commands
import rocks.ip
import os.path

class command(rocks.commands.HostArgumentProcessor,
		rocks.commands.report.command):
	pass

class Command(command):
	"""
	Report the host to IP address mapping in the form suitable for
	/etc/ssh/shosts.equiv

	<example cmd='report shosts'>
	Outputs lists of IPs to be used for /etc/ssh/shosts.equiv
	</example>
	"""
      
	def run(self, param, args):
		self.beginOutput()
		self.addOutput('localhost', '<file name="/etc/ssh/shosts.equiv">')
		self.addOutput('localhost', '# Added by rocks report shosts #')
		self.addOutput('localhost', '#        DO NOT MODIFY       #')

		gen = self.db.getHostAttr('localhost', 'rocks_autogen_user_keys')
		self.addOutput('localhost', '# rocks_autogen_user_keys: %s' % gen)

		# Grab all IPs in the database
		cmd = 'SELECT ip FROM networks WHERE ip IS NOT NULL;'
		self.db.execute(cmd)

		if gen is None or gen.lower() != 'true':
			for ip,  in self.db.fetchall():
				# Construct the shosts entry we only use the ip
				h = '%s' % (ip)
				self.addOutput('localhost', h)
		
		self.addOutput('localhost', '</file>')
		self.endOutput(padChar='')
