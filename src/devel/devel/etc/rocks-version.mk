#
# $Id: rocks-version.mk,v 1.9 2012/02/01 19:45:03 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# $Log: rocks-version.mk,v $
# Revision 1.9  2012/02/01 19:45:03  phil
# Support python 2.4 on 5, 2.6 on 6. Split out the rocks version major, minor and release name to a separate file (rocks-version-common.mk) used by both python.mk and rocks-version.mk
#
# Revision 1.8  2012/01/23 19:57:50  phil
# Updates for rpm version 4
# Set Rocks version to 6.0
# XXX -- Version should really be set from a bootstrap build to we can easily
# flip between 5 and 6 builds. editing rocks-version.mk is cumbersome
#
# Revision 1.7  2011/11/11 06:00:25  phil
# Updated anaconda to RHEL 5.7 base
#
# Revision 1.6  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.5  2011/04/15 19:41:59  phil
# Updates to build under CentOS 5.6 and new anaconda version.
# Calling this version5.4.3. Codename Viper.
#
# Had to rebuild our own kudzu lib because the CentOS 5.6 version on initial
# release was bad. See bug ID 4813 on bugs.centos.org. That was a not fun debug.
#
# Splash screen is work in progress.
#
# Revision 1.4  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.3  2010/08/05 19:00:03  bruno
# permission to buzz the tower
#
# Revision 1.2  2010/08/04 23:37:28  bruno
# next version
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.36  2010/04/13 20:01:16  mjk
# long date for PUBDATE
#
# Revision 1.35  2009/10/15 19:12:44  bruno
# just rolled, not three
#
# Revision 1.34  2009/10/08 16:36:28  bruno
# version bump
#
# Revision 1.33  2009/05/01 19:06:46  mjk
# chimi con queso
#
# Revision 1.32  2008/12/23 18:05:52  bruno
# bump release number and name
#
# Revision 1.31  2008/10/18 00:55:43  mjk
# copyright 5.1
#
# Revision 1.30  2008/09/24 19:46:20  bruno
# V.I
#
# Revision 1.29  2008/03/06 23:41:29  mjk
# copyright storm on
#
# Revision 1.28  2007/12/17 17:49:08  bruno
# take the space out of the version
#
# Revision 1.27  2007/12/13 02:53:40  bruno
# can now build a bootable kernel CD and build a physical frontend with V
# on RHEL 5 update 1
#
# Revision 1.26  2007/12/03 19:54:41  bruno
# wee bee vee
#
# Revision 1.25  2007/06/19 21:39:53  mjk
# dump-names more complete
#
# Revision 1.24  2007/06/05 22:07:48  bruno
# go from 4.3.0 to 4.3
#
# also fix for two-word release name
#
# Revision 1.23  2007/06/04 19:43:49  bruno
# must quote two-word release names
#
# Revision 1.22  2007/06/01 16:40:03  bruno
# rocks 4.3, Mars Hill
#
# Revision 1.21  2007/01/12 22:56:07  mjk
# more 3.8.1 fixes
#
# Revision 1.20  2006/09/07 02:41:08  mjk
# added patch version for 4.2.1
#
# Revision 1.19  2006/08/15 19:10:48  mjk
# doc additions
#
# Revision 1.18  2006/08/10 00:09:14  mjk
# 4.2 copyright
#
# Revision 1.17  2006/06/18 19:43:23  bruno
# bump rocks name and version number
#
# Revision 1.16  2006/01/15 21:33:02  mjk
# SOUTH korea
#
# Revision 1.15  2005/12/08 00:20:36  mjk
# Baitou, Korea
#
# Revision 1.14  2005/10/18 20:20:30  bruno
# automatically set the copyright date
#
# Revision 1.13  2005/10/12 18:08:21  mjk
# final copyright for 4.1
#
# Revision 1.12  2005/10/05 18:40:41  bruno
# added ROCKS_TAG variable
#
# Revision 1.11  2005/09/16 01:02:00  mjk
# updated copyright
#
# Revision 1.10  2005/08/31 01:08:23  bruno
# back to just 'Fuji'
#
# Revision 1.9  2005/08/25 18:55:24  mjk
# *** empty log message ***
#
# Revision 1.8  2005/06/27 23:34:24  mjk
# *** empty log message ***
#
# Revision 1.7  2005/06/27 21:56:06  mjk
# Next release is fuji/4.1
#
# Revision 1.6  2005/03/28 23:58:32  mjk
# added ROCKS_VERSION
#
# Revision 1.5  2005/03/14 18:40:57  bruno
# bump versions for the next release
#
# Revision 1.4  2005/03/12 01:21:08  fds
# The next mountain to climb.
#
# Revision 1.3  2004/10/21 01:32:58  mjk
# add PUBDATE for usersguides
#
# Revision 1.2  2004/10/21 01:18:16  mjk
# VERSION_NAME is same as RELEASE_NAME
#
# Revision 1.1  2004/09/10 17:56:51  bruno
# new way (and hopefully easier) to set new rocks version number
#
# Revision 1.19  2004/07/28 23:23:23  fds
# Typo
#
# Revision 1.18  2004/07/24 17:07:37  fds
# The usual drill. New name (rhymes with sheepie-poo), will make a beautiful
# disk image. We'll keep the old version number for a bit longer.
#
# Revision 1.17  2004/03/25 03:15:08  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.16  2004/02/09 22:41:17  fds
# Cannot uppercase this here, dont try. (rocksrc files).
#
# Revision 1.15  2004/02/04 00:26:25  fds
# Cali over those tree-hugging stoners in Colorado
#
# Revision 1.14  2004/02/03 21:31:05  fds
# Name stays, version number backed down to not mess with us until we're ready
#
# Revision 1.13  2004/02/03 21:12:10  fds
# Rocks 3.2.0 release name. Shavano is a Colorado fourteener, named after a Ute Indian Chief.
#
# Revision 1.12  2003/09/23 01:34:40  fds
# Bumped version number and name. The Matterhorn
# is a famous mountain in the Swiss Alps near Zermatt. It has a very recognizable
# and admired profile.
#
# Revision 1.11  2003/09/15 17:25:58  fds
# Using python.mk in /etc to find Py version.
#
# Revision 1.10  2003/09/12 21:44:04  fds
# Adding Python variables
#
# Revision 1.9  2003/07/26 17:30:03  bruno
# new version - 3.0.0
#
# Revision 1.8  2003/05/22 16:45:33  mjk
# 2.3.3 starts here
#
# Revision 1.7  2003/03/11 21:08:44  mjk
# added PROJECT_NAME
#
# Revision 1.6  2003/02/26 22:47:56  fds
# Changed 2.3.2 release name to Annapurna.
#
# Revision 1.5  2003/02/25 22:13:27  fds
# Bumped version to 2.3.2 (K2).
#
# Revision 1.4  2003/01/27 21:17:58  fds
# Added release name.
#
# Revision 1.3  2003/01/24 21:13:37  fds
# Added micro number
#
# Revision 1.2  2002/10/18 21:33:25  mjk
# Rocks 2.3 Copyright
#
# Revision 1.1  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
#

ifndef __RELEASE_MK
__RELEASE_MK = yes

-include $(ROCKSROOT)/etc/rocks-version-common.mk
include rocks-version-common.mk

ifeq ($(VERSION.PATCH),)
VERSION   = $(VERSION.MAJOR).$(VERSION.MINOR)
ROCKS_TAG = ROCKS_$(VERSION.MAJOR)_$(VERSION.MINOR)
else
VERSION   = $(VERSION.MAJOR).$(VERSION.MINOR).$(VERSION.PATCH)
ROCKS_TAG = ROCKS_$(VERSION.MAJOR)_$(VERSION.MINOR)_$(VERSION.PATCH)
endif
ROCKS_VERSION = $(VERSION)

# The project name is used to identify to distribution.  The base 
# distribution is controlled by the "rocks" projects.  If you want to
# build you own distribution and differentiate it from the parent
# distribution change this variable.  This is used by the anaconda
# loader as an attribute on the URL kickstart request line.

PROJECT_NAME = rocks

# All docbook stuff include a publication date, let make this global
# right here.

PUBDATE = $(shell date +'%b %d %Y')
YEAR = $(shell date +'%Y')

rocks-copyright.txt:
	rm -f $@
	touch $@
	@echo '@Copyright@' >> $@
	@echo '' >> $@
	@echo '				Rocks(r)' >> $@
	@echo '		         www.rocksclusters.org' >> $@
	@echo '		         version 5.4.3 (Viper)' >> $@
	@echo '' >> $@
	@echo 'Copyright (c) 2000 - 2011 The Regents of the University of California.' >> $@
	@echo 'All rights reserved.	' >> $@
	@echo '' >> $@
	@echo 'Redistribution and use in source and binary forms, with or without' >> $@
	@echo 'modification, are permitted provided that the following conditions are' >> $@
	@echo 'met:' >> $@
	@echo '' >> $@
	@echo '1. Redistributions of source code must retain the above copyright' >> $@
	@echo 'notice, this list of conditions and the following disclaimer.' >> $@
	@echo '' >> $@
	@echo '2. Redistributions in binary form must reproduce the above copyright' >> $@
	@echo 'notice unmodified and in its entirety, this list of conditions and the' >> $@
	@echo 'following disclaimer in the documentation and/or other materials provided ' >> $@
	@echo 'with the distribution.' >> $@
	@echo '' >> $@
	@echo '3. All advertising and press materials, printed or electronic, mentioning' >> $@
	@echo 'features or use of this software must display the following acknowledgement: ' >> $@
	@echo '' >> $@
	@echo '	"This product includes software developed by the Rocks(r)' >> $@
	@echo '	Development Team at the San Diego Supercomputer Center at the' >> $@
	@echo '	University of California, San Diego and its contributors."' >> $@
	@echo '' >> $@
	@echo '4. Except as permitted for the purposes of acknowledgment in paragraph 3,' >> $@
	@echo 'neither the name or logo of this software nor the names of its' >> $@
	@echo 'authors may be used to endorse or promote products derived from this' >> $@
	@echo 'software without specific prior written permission.  The name of the' >> $@
	@echo 'software includes the following terms, and any derivatives thereof:' >> $@
	@echo '"Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of ' >> $@
	@echo 'the associated name, interested parties should contact Technology ' >> $@
	@echo 'Transfer & Intellectual Property Services, University of California, ' >> $@
	@echo 'San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, ' >> $@
	@echo 'Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu' >> $@
	@echo '' >> $@
	@echo 'THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''' >> $@
	@echo 'AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,' >> $@
	@echo 'THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR' >> $@
	@echo 'PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS' >> $@
	@echo 'BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR' >> $@
	@echo 'CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF' >> $@
	@echo 'SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR' >> $@
	@echo 'BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,' >> $@
	@echo 'WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE' >> $@
	@echo 'OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN' >> $@
	@echo 'IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.' >> $@
	@echo '' >> $@
	@echo '@Copyright@' >> $@
	-cat $@ | grep -v "^@Copyright" | expand -- > $@


rocks-version.mk: $(wildcard $(ROCKSROOT)/etc/rocks-version.mk)
	cp $^ $@

clean::
	-rm rocks-version.mk rocks-copyright.txt

endif
