#!/bin/bash
#
# $Id: iso-backup.cron.sh,v 1.11 2010/09/07 23:52:48 bruno Exp $
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
# $Log: iso-backup.cron.sh,v $
# Revision 1.11  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.10  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.9  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.8  2008/03/06 23:41:33  mjk
# copyright storm on
#
# Revision 1.7  2007/06/23 04:03:20  mjk
# mars hill copyright
#
# Revision 1.6  2006/09/11 22:47:03  mjk
# monkey face copyright
#
# Revision 1.5  2006/08/10 00:09:26  mjk
# 4.2 copyright
#
# Revision 1.4  2005/10/12 18:08:32  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:02:12  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:21:48  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:42  mjk
# moved from core to base
#
# Revision 1.5  2004/03/25 03:15:15  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.4  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.3  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.2  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.1  2003/01/16 23:02:22  mjk
# *** empty log message ***
#


# Since we are just going to run this every night just dump all errors
# and warning to /dev/null.  I don't need the extra cron bitchy
# emails.

@PKGROOT@/bin/iso-backup > /dev/null 2>&1

