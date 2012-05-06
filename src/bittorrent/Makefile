#
# $Id: Makefile,v 1.14 2012/05/06 05:48:18 phil Exp $
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
# $Log: Makefile,v $
# Revision 1.14  2012/05/06 05:48:18  phil
# Copyright Storm for Mamba
#
# Revision 1.13  2011/07/23 02:30:24  phil
# Viper Copyright
#
# Revision 1.12  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.11  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.10  2009/10/07 16:58:49  bruno
# set ROCKSROOT
#
# Revision 1.9  2009/08/24 14:53:58  bruno
# more
#
# Revision 1.8  2006/12/06 00:20:20  anoop
# All the Makefiles get a bit of an overhaul
#
# $(INSTALL) is used instead of install
# $(MAKE) is used instead of make or gmake
# $(TAR) is used instead of tar of gtar
#
# The mode argument for the $(INSTALL) command needs to be numeric and
# follow the convention of
#
# install [-cs] [-g group] [-m mode] [-o owner] file ...  destination
# install  -d   [-g group] [-m mode] [-o owner] dir
#
# This is portable across solaris and linux.
#
# Finally "tar xzf $TARFILE.tar.gz" is replaced with "gunzip -c $TARFILE.tar.gz | tar -xf -"
# This is again done for portability.
#
# This needs to be the convention from now on.
#
# Revision 1.7  2006/12/02 01:04:53  anoop
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
# Revision 1.6  2005/12/30 19:35:25  mjk
# removed some of the specfiles
#
# Revision 1.5  2005/09/02 00:05:48  bruno
# pushing toward 4.1 beta
#
# Revision 1.4  2005/08/24 01:23:10  bruno
# added 'done' command
#
#

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

-include $(ROCKSROOT)/etc/python.mk
include python.mk


build:

install::
	mkdir -p $(ROOT)/$(PY.ROCKS)/BitTorrent

	gunzip -c $(BT_NAME)-$(BT_VERSION).tar.gz | $(TAR) xf -
	( cd $(BT_NAME)-$(BT_VERSION)/$(BT_NAME) && \
					cp *py $(ROOT)/$(PY.ROCKS)/BitTorrent )
	( cd patch-files/$(BT_NAME) && cp *py $(ROOT)/$(PY.ROCKS)/BitTorrent )

	cp rocks.py $(ROOT)/$(PY.ROCKS)/BitTorrent

	mkdir -p $(ROOT)/opt/rocks/bittorrent
	(cd $(BT_NAME)-$(BT_VERSION) && cp *py $(ROOT)/opt/rocks/bittorrent)
	(cd patch-files && cp *py $(ROOT)/opt/rocks/bittorrent)
	cp rocks-*.py $(ROOT)/opt/rocks/bittorrent

	mkdir -p $(ROOT)/etc/rc.d/init.d
	cp init.d/rocks-bittorrent $(ROOT)/etc/rc.d/init.d

clean::
	rm -rf $(BT_NAME)-$(BT_VERSION)
	rm -f $(NAME).spec.in

