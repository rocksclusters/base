#
# DHCP insert-ethers plugin module
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
# $Log: 01-dhcpd.py,v $
# Revision 1.18  2012/05/06 05:48:49  phil
# Copyright Storm for Mamba
#
# Revision 1.17  2011/07/23 02:30:50  phil
# Viper Copyright
#
# Revision 1.16  2010/11/19 23:56:00  bruno
# convert dhcp configuration to output XML
#
# lookup the private interface name and write it to /etc/sysconfig/dhcpd
#
# Revision 1.15  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.14  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.13  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.12  2008/05/22 21:02:07  bruno
# rocks-dist is dead!
#
# moved default location of distro from /export/home/install to
# /export/rocks/install
#
# Revision 1.11  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.10  2007/06/23 04:03:26  mjk
# mars hill copyright
#
# Revision 1.9  2006/09/15 02:38:21  mjk
# removed ROCK_ROOT variable, #80 (trac.rocksclusters.org)
#
# Revision 1.8  2006/09/11 22:47:30  mjk
# monkey face copyright
#
# Revision 1.7  2006/09/11 18:02:52  bruno
# make sure certain code is not run when '--batch' or '--norestart' flags
# are thrown.
#
# this addresses ticket #64 (trac.rocksclusters.org).
#
# Revision 1.6  2006/08/10 00:09:46  mjk
# 4.2 copyright
#
# Revision 1.5  2005/10/12 18:08:47  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:26  mjk
# updated copyright
#
# Revision 1.3  2005/05/27 22:34:56  fds
# Insert-ethers plugins also get node id for added(), removed().
#
# Revision 1.2  2005/05/24 21:22:01  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/14 20:25:18  fds
# Plugin architecture: service control is modular. Rolls can add hooks without
# touching insert-ethers itself. Plugins can be ordered relative to each other by
# filename.
#
#

import os
import rocks.sql

class Plugin(rocks.sql.InsertEthersPlugin):
	"Controls the DHCP server when nodes are added and removed."

	def added(self, nodename, id):
		self.restart()

	def removed(self, nodename, id):
		self.restart()

	def update(self):
		self.restart()

	def done(self):
		pass

	def restart(self):
		if '--batch' in self.app.caller_args or \
				'--norestart' in self.app.caller_args:
			return

		cmd = '/opt/rocks/bin/rocks report host dhcpd localhost | '
		cmd += '/opt/rocks/bin/rocks report script | bash'
		os.system(cmd)

		os.system('/etc/rc.d/init.d/dhcpd restart > /dev/null 2>&1')
