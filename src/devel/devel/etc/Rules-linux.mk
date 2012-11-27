# $Id: Rules-linux.mk,v 1.6 2012/11/27 00:48:32 phil Exp $
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
# $Log: Rules-linux.mk,v $
# Revision 1.6  2012/11/27 00:48:32  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.5  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.4  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.3  2011/06/16 17:59:32  anoop
# Moving away from foundation-perl
#
# Revision 1.2  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.22  2009/05/01 19:06:46  mjk
# chimi con queso
#
# Revision 1.21  2008/10/18 00:55:43  mjk
# copyright 5.1
#
# Revision 1.20  2008/03/06 23:41:29  mjk
# copyright storm on
#
# Revision 1.19  2007/11/29 01:58:09  anoop
# use PATCH variable instead of patch
#
# Revision 1.18  2007/06/19 21:39:53  mjk
# dump-names more complete
#
# Revision 1.17  2007/04/28 00:28:10  anoop
# *** empty log message ***
#
# Revision 1.16  2007/01/12 22:56:07  mjk
# more 3.8.1 fixes
#
# Revision 1.15  2006/09/07 02:41:08  mjk
# added patch version for 4.2.1
#
# Revision 1.14  2006/08/10 00:09:14  mjk
# 4.2 copyright
#
# Revision 1.13  2006/08/07 18:22:59  mjk
# added python and perl variables
#
# Revision 1.12  2006/07/05 23:08:40  mjk
# fix make roll target
#
# Revision 1.11  2006/06/05 21:14:17  mjk
# enable suse building
#
# Revision 1.10  2006/01/17 04:33:43  mjk
# *** empty log message ***
#
# Revision 1.9  2006/01/16 23:18:04  mjk
# - python 2.4
# - rpm debugging tools
#
# Revision 1.8  2006/01/16 06:25:16  mjk
# first pass at solaris packages
#
# Revision 1.7  2006/01/15 22:32:33  mjk
# - Buildroot is in localdir, this makes cleanup on failed RPM builds easier
# - Generated specfile has no %clean section
# - Makefile does clean instead
# - $(NAME).pkg is the RPM tree, you can check this before installing the RPM.
#   Same idea as the distN directory for rolls.
# - Theme is less like RPM, and simpler debugging
#
# Revision 1.6  2006/01/15 22:15:01  mjk
# *** empty log message ***
#
# Revision 1.5  2006/01/15 21:59:37  mjk
# move away from template file
#
# Revision 1.4  2005/12/31 18:28:47  mjk
# The last change to prefix the wrapper tarball with an '_' works but is more
# invasive than required.  Instead we just exclude the symlink package name
# from the tarball and get the same result.  A simple one line change in just
# one file.  This also means all existing spec files should still work, so
# this change will not break CVS.
#
# Revision 1.3  2005/12/31 04:05:33  mjk
# fix SEDSPEC for roll profile RPM
#
# Revision 1.2  2005/12/31 03:31:14  mjk
# moved stuff in linux makefile
#
# Revision 1.1  2005/12/30 22:25:27  mjk
# *** empty log message ***
#

ifndef __RULES_LINUX_MK
__RULES_LINUX_MK = yes

# --------------------------------------------------------------------- #
# OS Dependent variables
# --------------------------------------------------------------------- #

PYTHON	= /opt/rocks/bin/python
WEBSERVER_ROOT = /var/www/html
PATCH	= patch
# --------------------------------------------------------------------- #
# Figure out what Linux distribution we are on
# --------------------------------------------------------------------- #

DISTRIBUTION.BIN = $(ROCKSROOT.ABSOLUTE)/bin/distribution
DISTRIBUTION = $(shell if [ ! -x ./_distribution ]; then \
		cp $(DISTRIBUTION.BIN) _distribution; fi; ./_distribution)

-include $(ROCKSROOT)/etc/Rules-$(OS)-$(DISTRIBUTION).mk
-include Rules-$(OS)-$(DISTRIBUTION).mk


# --------------------------------------------------------------------- #
# Copy this file into the tarball release
# --------------------------------------------------------------------- #
Rules-linux.mk: $(wildcard $(ROCKSROOT)/etc/Rules-linux.mk)
	cp $^ $@

clean::
	-rm Rules-linux.mk _distribution

endif	#__RULES_LINUX_MK
