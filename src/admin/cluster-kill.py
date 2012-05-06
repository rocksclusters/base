#! @PYTHON@
#
# $Id: cluster-kill.py,v 1.15 2012/05/06 05:48:17 phil Exp $
#
# kill a set of processes on cluster nodes which match the regular expression
# in supplied on the command line
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
# $Log: cluster-kill.py,v $
# Revision 1.15  2012/05/06 05:48:17  phil
# Copyright Storm for Mamba
#
# Revision 1.14  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.13  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.12  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:19  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:47:02  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:25  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:48:55  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:32  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:11  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:32  mjk
# use rocks version of python
#
# Revision 1.2  2005/05/24 21:21:47  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:41  mjk
# moved from core to base
#
# Revision 1.10  2004/03/25 03:15:14  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.9  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.8  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.7  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.6  2002/10/18 21:33:25  mjk
# Rocks 2.3 Copyright
#
# Revision 1.5  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.4  2001/11/08 18:42:07  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.3  2001/11/01 20:50:02  bruno
# update to cluster-kill
#
# Revision 1.2  2001/10/11 00:20:36  bruno
# 'self' realization (from newport!)
#
# Revision 1.1  2001/10/02 03:53:04  mjk
# - Added DISPLAY check for shoot-node
# - Moved over cluster-* suite of tools from cluster-config
#
# Revision 1.5  2001/06/27 22:33:48  mjk
# OOPSed the code
#
# Revision 1.4  2001/06/21 15:27:45  bruno
# changed cut to awk
#
# Revision 1.3  2001/05/18 20:16:06  bruno
# needed to provide more of a path to clusterfork object
#
# Revision 1.2  2001/05/09 20:17:14  bruno
# bumped copyright 2.1
#
# Revision 1.1  2001/05/05 00:50:03  bruno
# re-release
#
#

import sys
import string
import rocks.pssh

class App(rocks.pssh.ClusterFork):

	def __init__(self, argv):
		rocks.pssh.ClusterFork.__init__(self, argv)
		self.usage_name		= 'Cluster Kill'
		self.usage_version	= '@VERSION@'

	def run(self):
		cmd = 'ps auwx | grep '
		cmd = cmd + string.join(self.getArgs())
		cmd = cmd + " | grep -v grep | awk '{print \$2}'"
		cmd = cmd + " | xargs kill -9"
		rocks.pssh.ClusterFork.run(self, cmd)

app = App(sys.argv)
app.parseArgs()
app.run()

