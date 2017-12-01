#
# Makefile for User defined 411 groups
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# $Log: Group.mk,v $
# Revision 1.11  2012/11/27 00:48:07  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.10  2012/10/18 17:55:21  phil
# 411 plugin for google authenticator.  creates a tar file of all keys (except
# root) and transfers to login appliances
#
# Revision 1.9  2012/10/16 21:21:36  phil
# add qrencode to build manifest and bootstrap.  Add google-authenticator key tokens toLogin appliance 411 files
#
# Revision 1.8  2012/10/02 21:10:12  clem
# Fix problem with spaces in group memebership of 411 service
#
# Problem reported by Scott Hamilton:
# http://marc.info/?l=npaci-rocks-discussion&m=134685806116850&w=2
#
# Revision 1.7  2012/05/06 05:48:16  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.5  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.4  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.3  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.1  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.8  2007/06/23 04:03:39  mjk
# mars hill copyright
#
# Revision 1.7  2006/09/11 22:48:49  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:10:54  mjk
# 4.2 copyright
#
# Revision 1.5  2005/10/12 18:09:43  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:03:20  mjk
# updated copyright
#
# Revision 1.3  2005/05/27 23:20:45  fds
# 411 Groups makefile validated. Needs docs.
#
# Revision 1.2  2005/05/24 21:22:45  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/04/21 21:41:25  fds
# Helper makefile for 411 groups.
#
#

GROUPS = Storage-Node Math-Node
GROUPS = Login

.PHONY: groups
groups: 
	@echo "# Generated, do not edit." > 411-Group.mk; \
	echo >> 411-Group.mk
	$(MAKE) $(GROUPS)


### Files for Google-Authenticator two-factor authentication. Sync
##    to Login nodes.
ALLKEYS = /export/google-authenticator/keys.tar
TOKENS = $(subst root,,$(ALLKEYS))
Login: 
	@echo "Rebuilding 411 Group makefile for $@..."
	@files="$(TOKENS)"; \
	echo "## $@ Group" >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	echo -n "all: " >> 411-Group.mk; \
	for f in $$files; do \
		echo -n "`$(PUT) --411name --chroot=/var/411/groups/$@ \
			--group=$@ $$f` "; \
	done >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	for f in $$files; do \
		echo "`$(PUT) --411name --chroot=/var/411/groups/$@ \
			--group=$@ $$f`:: $$f"; \
		echo "	$(PUT) --group=$@ --chroot=/var/411/groups/$@ \$$?"; \
		echo; \
	done >> 411-Group.mk
#
# Example group1. These files will be sent to nodes in a group
# called "Storage-Node". If you make a /var/411/groups/Storage-Node/etc/passwd
# file, it will appear on the node as /etc/passwd.
# Node are assigned to a group based upon their membership, if the membership 
# contains spaces, they will be converted into _. 
# So NAS Appliance belongs to the 411 group NAS_Appliance
#
STORAGE_NODE_FILES = \
	/var/411/groups/Storage-Node/etc/storage-passwd \
	/var/411/groups/Storage-Node/etc/storage-group \

Storage-Node:
	@echo "Rebuilding 411 Group makefile for $@..."
	@files="$(STORAGE_NODE_FILES)"; \
	echo "## $@ Group" >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	echo -n "all: " >> 411-Group.mk; \
	for f in $$files; do \
		echo -n "`$(PUT) --411name --chroot=/var/411/groups/$@ \
			--group=$@ $$f` "; \
	done >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	for f in $$files; do \
		echo "`$(PUT) --411name --chroot=/var/411/groups/$@ \
			--group=$@ $$f`:: $$f"; \
		echo "	$(PUT) --group=$@ --chroot=/var/411/groups/$@ \$$?"; \
		echo; \
	done >> 411-Group.mk


#
# Second example group. These files will be sent to nodes in a group
# called "Math-Node". The /var/411/groups/Math-Node/etc/passwd
# file will appear on the node as /etc/passwd.
#
MATH_NODE_FILES = \
	/var/411/groups/Math-Node/etc/passwd \
	/var/411/groups/Math-Node/etc/group \
	/var/411/groups/Math-Node/etc/shadow

Math-Node:
	@echo "Rebuilding 411 Group makefile for $@..."
	@files="$(MATH_NODE_FILES)"; \
	echo "## $@ Group" >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	echo -n "all: " >> 411-Group.mk; \
	for f in $$files; do \
		echo -n "`$(PUT) --411name --chroot=/var/411/groups/$@ \
			--group=$@ $$f` "; \
	done >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	echo >> 411-Group.mk; \
	for f in $$files; do \
		echo "`$(PUT) --411name --chroot=/var/411/groups/$@ \
			--group=$@ $$f`:: $$f"; \
		echo "	$(PUT) --group=$@ --chroot=/var/411/groups/$@ \$$?"; \
		echo; \
	done >> 411-Group.mk

#
# Repeat the above two paragraphs for each group you need.
#


