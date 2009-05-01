#! @PYTHON@
#
# $Id: add-new-appliance.py,v 1.15 2009/05/01 19:07:09 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: add-new-appliance.py,v $
# Revision 1.15  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.14  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.13  2008/04/02 16:59:37  bruno
# nuke dead commands
#
# put message in other commands that point the user to the appropriate rocks
# command-line command.
#
# Revision 1.12  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.11  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:47:28  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.8  2006/07/06 19:50:11  bruno
# for 'dump' command, print name of utility from argv -- that way, we can
# specify the full pathname when these tools are used during an installation
# and the path has not yet been initialized.
#
# Revision 1.7  2006/06/02 17:36:47  bruno
# added ability to set membership name independently of the appliance name
#
# Revision 1.6  2006/01/16 06:49:01  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:46  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:25  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:37  mjk
# use rocks version of python
#
# Revision 1.2  2005/05/24 21:22:00  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:03:17  mjk
# moved from core to base
#
# Revision 1.7  2005/02/10 06:47:47  phil
# Now sports --dump command.
# Also, added --graph argument, --dryrun.
# really needs a --distribution flag, too.
# Eventually, we should write a modify-appliance.py
#
# Revision 1.6  2005/02/01 17:52:37  fds
# Added the --shortname option for the appliance table.
#
# Revision 1.5  2004/11/30 01:30:42  fds
# Added compute and public control. Fully tested repeat insert protection.
# Note: sys.exit call also raises an exception.
#
# Revision 1.4  2004/09/02 20:41:17  bruno
# translate the user-supplied appliance name to a basename
# that will be used for the node name.
#
# for example, 'Tile Display' is translated to 'tile-display'
#
# Revision 1.3  2004/09/02 18:41:04  bruno
# remove more debug
#
# Revision 1.2  2004/09/02 18:36:37  bruno
# nuke debug statements
#
# Revision 1.1  2004/08/16 22:16:08  bruno
# a script to easily add a new appliance (and subsequently a new membership)
# to the frontend's database
#
#

print 'add-new-appliance is no longer supported. please use:'
print '\n\trocks add appliance\n'
