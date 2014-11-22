# $Id: tentakel.py,v 1.9 2012/11/27 00:48:51 phil Exp $
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
# $Log: tentakel.py,v $
# Revision 1.9  2012/11/27 00:48:51  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.8  2012/05/06 05:48:49  phil
# Copyright Storm for Mamba
#
# Revision 1.7  2011/07/23 02:30:51  phil
# Viper Copyright
#
# Revision 1.6  2010/09/07 23:53:10  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:07:10  mjk
# chimi con queso
#
# Revision 1.4  2009/03/24 22:24:04  bruno
# moved 'dbreport tentakel' to rocks command line
#
# Revision 1.3  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 22:44:44  bruno
# moved tentakel from the hpc to the base roll
#
# Revision 1.5  2007/06/23 04:03:45  mjk
# mars hill copyright
#
# Revision 1.4  2006/09/11 22:48:55  mjk
# monkey face copyright
#
# Revision 1.3  2006/09/11 18:06:08  bruno
# don't call restart() when '--batch' or '--norestart' flags are used.
#
# Revision 1.2  2006/08/10 00:11:00  mjk
# 4.2 copyright
#
# Revision 1.1  2005/12/30 05:58:30  mjk
# added insert-ethers plugin
#

import os
import rocks.sql

class Plugin(rocks.sql.InsertEthersPlugin):
	"tentakel plugin for Insert Ethers"

	def added(self, nodename):
		self.update()

	def removed(self, nodename):
		self.update()

	def update(self):
		cmd = '/opt/rocks/bin/rocks report tentakel '
		cmd += '> /etc/tentakel.conf'
		os.system(cmd)

