#
# $Id: Makefile,v 1.14 2011/11/07 18:33:59 phil Exp $
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
# $Log: Makefile,v $
# Revision 1.14  2011/11/07 18:33:59  phil
# Make checkout from CVS optional. Default to expecting that restore roll
# is in local tree (common when building rocks itself)
#
# Revision 1.13  2011/07/23 02:30:44  phil
# Viper Copyright
#
# Revision 1.12  2010/09/07 23:53:05  bruno
# star power for gb
#
# Revision 1.11  2010/06/29 21:07:53  bruno
# build fixes
#
# Revision 1.10  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.9  2009/05/01 19:07:05  mjk
# chimi con queso
#
# Revision 1.8  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.7  2008/08/29 20:01:55  mjk
# - Allow not just bruno to build the package
# - Use the /opt/rocks/share build env for restore roll
#
# Revision 1.6  2007/06/14 17:28:42  bruno
# cvs.rocksclusters.org doesn't hold the head of the tree
#
# Revision 1.5  2006/12/02 01:04:53  anoop
# Ridiculously big ass commit.
# Also known as the week after thanksgiving 2006. Or "The day Anoop
# broke Rocks".
#
# Main Changes.
#
# 1. Added a roll-profile.mk file. This is meant as a makefile for building
# the profile rpm containing all the XML files meant for the roll. This is a
# breakaway from the spec.in file method of building the profile RPM.
#
# 2. The variable PWD is now changed to CURDIR. The main reason for this is
# PWD is supplied by the shell. CURDIR is the variable supplied by gmake itself.
# This means we can have a slightly more platform independant way of doing things.
# Also Solaris was failing to set PWD correctly in the source directories, wreaking
# havoc on the location of the BUILD and PKG directories.
#
# Revision 1.4  2006/07/26 20:29:18  bruno
# make sure to prune the directories when we check them out
#
# Revision 1.3  2006/07/14 04:45:09  phil
# Add TAG to get specific version of the repository
#
# Revision 1.2  2006/06/24 00:26:09  nadya
# use variable for cvs
#
# Revision 1.1  2005/12/14 21:13:49  bruno
# create an RPM that has:
#
#  - minimum number of files and tree structure in order to build a roll
#  - the 'template' roll (to serve as an example of how to build a roll)
#  - the 'restore' roll (used to backup the important info in your cluster)
#
# Revision 1.1  2005/12/13 04:59:41  bruno
# the start of the 'frontend restore' roll
#
#

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = $(CURDIR)/../../src/devel/devel

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

-include $(ROCKSROOT)/etc/python.mk
include python.mk

CVSROOT = -d $(USER)@fyp.rocksclusters.org:/home/cvs/CVSROOT
TAG =
# uncomment/change for Release
# TAG = -r ROCKS_4_2
# uncomment if you want to checkout the latest restore roll instead of
# copying from the local
# RETRIEVECVS = True


pretar::
	( if [ ! -d rocks/src/roll/restore ]; then \
		mkdir -p rocks/src/roll/restore; \
	fi )
	(cd ../../../restore; $(TAR) cf - * ) | \
		(cd rocks/src/roll/restore; $(TAR) xvfBp - ) 
build:
	( if [ "x$(RETRIEVECVS)" == "xTrue" ]; then \
		if [ -d rocks ]; then /bin/rm -r rocks; fi; \
		$(CVS) $(CVSROOT) checkout -P $(TAG) rocks/src/roll/restore; \
	  fi \
	)
	for i in `find . -type d -name CVS` ; do \
		rm -rf $$i ; \
	done
	(cd rocks/src/roll/restore; $(MAKE) clean )

install::
	mkdir -p $(ROOT)/export/site-roll/
	cp -R rocks $(ROOT)/export/site-roll/

clean::
	/bin/rm -rf rocks

