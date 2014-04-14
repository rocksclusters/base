#
# Makefile to publish /etc login files via the 411
# Secure Information Service.
#
# Make ensures that we do not republish unchanged files.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
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
# $Log: Makefile,v $
# Revision 1.9  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.8  2012/05/06 05:48:16  phil
# Copyright Storm for Mamba
#
# Revision 1.7  2011/07/23 02:30:23  phil
# Viper Copyright
#
# Revision 1.6  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.3  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.2  2008/02/15 00:06:48  mjk
# - Apply the HG Changeset from Takahiro Hirofuchi (AIST)
# - Modified changeset to ignore services and rpc files
#
# # HG changeset patch
# # User root@vizzy.rocksclusters.org
# # Date 1203022614 28800
# # Node ID fc6e0b98fef1a65932eef3e5e5ad2bedf5b634b4
# # Parent  2716de75af4304c3e3d261fb9cf19a1c8d988f56
# Fix too slow booting bug caused by overrunning of vol_id.
# Remove comment headers from /etc/{passwd,group,shadow} because udev's
# vol_id cannot parse it correctly.
#
# Revision 1.1  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.9  2007/06/23 04:03:39  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:48:49  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:10:54  mjk
# 4.2 copyright
#
# Revision 1.6  2005/10/12 18:09:43  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:03:20  mjk
# updated copyright
#
# Revision 1.4  2005/05/27 23:20:45  fds
# 411 Groups makefile validated. Needs docs.
#
# Revision 1.3  2005/05/24 21:22:45  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/04/21 21:41:25  fds
# Helper makefile for 411 groups.
#
#

# The 411 publisher.
PUT=/opt/rocks/sbin/411put

# Normally we should send an alert on the Ganglia multicast channel.
SENDALERT = 1

ifeq ($(SENDALERT), 0)
PUT+= --noalert
endif

include Files.mk
-include 411.mk

411.mk: Makefile Files.mk
	touch $+
	@echo "Regenerating 411.mk..."
	@files="$(FILES)"; \
	files_nocomment="$(FILES_NOCOMMENT)"; \
	echo "# Generated, do not edit." > 411.mk; \
	echo >> 411.mk; \
	echo -n "all: " >> 411.mk; \
	for f in $$files $$files_nocomment; do \
		echo -n "`$(PUT) --411name $$f` "; \
	done >> 411.mk; \
	echo >> 411.mk; \
	echo >> 411.mk; \
	for f in $$files; do \
		echo "`$(PUT) --411name $$f`:: $$f"; \
		echo "	$(PUT) --comment=\"#\" \$$?"; \
		echo; \
	done >> 411.mk; \
	for f in $$files_nocomment; do \
		echo "`$(PUT) --411name $$f`:: $$f"; \
		echo "	$(PUT) --nocomment \$$?"; \
		echo; \
	done >> 411.mk


-include Group.mk
-include 411-Group.mk


restart force nuke:
	rm -rf /etc/411.d/*
	$(MAKE)

clean:
	rm -f 411.mk
	rm -f 411-Group.mk
