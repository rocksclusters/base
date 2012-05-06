# $Id: Rules-sunos.mk,v 1.4 2012/05/06 05:48:39 phil Exp $
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

# $Log: Rules-sunos.mk,v $
# Revision 1.4  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.2  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.15  2009/11/30 17:18:01  bruno
# for anoop
#
# Revision 1.14  2009/11/21 00:36:42  bruno
# Use /usr/bin/cc for compiling rather than /opt/SUNWspro.
# The path /usr is stable across versions.
#
# Revision 1.13  2009/07/27 21:38:12  anoop
# Added better support for contributed packages to Solaris
#
# Revision 1.12  2009/05/01 19:06:46  mjk
# chimi con queso
#
# Revision 1.11  2008/12/17 18:27:59  anoop
# MPIROOT Variable upgraded
#
# Revision 1.10  2008/11/30 19:20:54  anoop
# Added MPIROOT variable
#
# Revision 1.9  2008/10/18 00:55:43  mjk
# copyright 5.1
#
# Revision 1.8  2008/07/29 20:26:53  anoop
# pkg target changed back to : from ::
#
# Revision 1.7  2008/07/28 16:08:08  anoop
# pkg target needs to be :: rather than :
#
# Revision 1.6  2008/05/20 02:51:55  anoop
# Merged back changes from hg. Now the makefile builds a little more cleanly
# and does not set unnecessary flags.
#
# Revision 1.5  2008/03/06 23:41:29  mjk
# copyright storm on
#
# Revision 1.4  2007/11/29 01:58:09  anoop
# use PATCH variable instead of patch
#
# Revision 1.3  2007/10/25 04:24:43  anoop
# More Sun Studio specific variables
#
# Revision 1.2  2007/10/03 22:31:45  anoop
# More solaris support.
# Package building now closer to what comes out of Sun. The packages
# created are now easy to distribute on CD
#
# Revision 1.1  2007/10/02 23:58:19  anoop
# Remove all references to solaris, and added references to sunos.
# This is to standardize the naming between the python scripts and
# the Makefiles. One less variable that I'll have to deal with.
#

ifndef __RULES_SUNOS_MK
__RULES_SUNOS_MK = yes

# --------------------------------------------------------------------- #
# OS Dependent Stuff
# --------------------------------------------------------------------- #
USERID	= $(shell /usr/xpg4/bin/id -u)
SHELL	= /bin/bash
INSTALL = /usr/ucb/install
CC	= /usr/bin/cc
CXX	= /usr/bin/CC
CFLAGS	=
CXXFLAGS = 
CPPFLAGS = 
MPIROOT	= /opt/SUNWhpc/HPC8.2.1/sun
LD	= /usr/ccs/bin/ld
LDFLAGS = 
MAKE	= gmake
AR	= /usr/ccs/bin/ar
PF	= @printf
CVS	= /opt/rocks/bin/cvs
TAR	= gtar
PATCH	= gpatch
INCLUDE_PROFILES = 1
TARGET_PKG = pkg
INIT_SCRIPTS_DIR = /lib/svc/method

SOL.ROOT = $(REDHAT.ROOT)
BUILD = $(SOL.ROOT)/BUILD
PKGS = $(SOL.ROOT)/PKGS
PROFILE_DIR = /
PERL = /opt/rocks/bin/perl
WEBSERVER_ROOT = /var/apache2/htdocs
graph_dir := $(OS)

export CC CXX CFLAGS CXXFLAGS CPPFLAGS MPIROOT LD LDFLAGS MAKE INSTALL PERL

# --------------------------------------------------------------------- #
# Build the $(NAME).pkg directory
# --------------------------------------------------------------------- #
ROOT    = $(BUILD)/$(NAME)-$(VERSION)/$(NAME).pkg

$(ROOT):
	rm -rf $(ROOT) $(BUILD)/$(NAME)-$(VERSION)
	mkdir -p $(ROOT)
        
.PHONY: pkg-mkdirs
pkg-mkdirs:
	if [ ! -x $(BUILD) ]; then mkdir -p $(BUILD); fi
	if [ ! -x $(PKGS) ]; then mkdir -p $(PKGS); fi

.PHONY: pkg
pkg: root-check pkg-mkdirs $(ROOT) build install
ifndef MAKE.iscontrib
pkg:
	(							\
		cd $(ROOT);					\
		rm -rf pkginfo;					\
		mkdir -p $(ROOT)/../install;			\
		touch $(ROOT)/../install/depend;		\
		echo "i pkginfo=pkginfo" >> ../prototype;	\
		echo "i depend=install/depend" >> ../prototype;	\
		find . -print | pkgproto >> ../prototype;	\
	)
	$(PF) "PKG=\"ROCKS$(NAME)\"\n" > $(ROOT)/../pkginfo
	$(PF) "NAME=\"$(NAME)\"\n" >> $(ROOT)/../pkginfo
	$(PF) "ARCH=\"$(ARCH)\"\n" >> $(ROOT)/../pkginfo
	$(PF) "VERSION=\"$(VERSION)\"\n" >> $(ROOT)/../pkginfo
	$(PF) "CATEGORY=\"application\"\n" >> $(ROOT)/../pkginfo
	$(PF) "VENDOR=\"$(VENDOR)\"\n" >> $(ROOT)/../pkginfo
	$(PF) "BASEDIR=\"/\"\n" >> $(ROOT)/../pkginfo
	$(PF) "CLASSES=\"none\"\n" >> $(ROOT)/../pkginfo
	$(PF) "PKG_SRC_NOVERIFY=none\n" >> $(ROOT)/../pkginfo
	$(PF) "PKG_DST_QKVERIFY=none\n" >> $(ROOT)/../pkginfo
	$(PF) "PKG_CAS_PASSRELATIVE=none\n" >> $(ROOT)/../pkginfo
	rm -rf $(PKGS)/ROCKS$(NAME);
	pkgmk -o -r $(ROOT) -f $(ROOT)/../prototype -d $(PKGS)/;
endif

clean::
	rm -rf $(ROOT) $(NAME).pkg 
	rm -rf ROCKS$(NAME) ROCKS$(NAME).$(VERSION).$(ARCH).pkg.tar.gz
	rm -rf ROCKS$(NAME)-$(ARCH)

# --------------------------------------------------------------------- #
# Copy this file into the tarball release
# --------------------------------------------------------------------- #
Rules-$(OS).mk: $(wildcard $(ROCKSROOT)/etc/Rules-$(OS).mk)
	cp $^ $@

clean::
	-rm Rules-$(OS).mk

endif	#__RULES_SUNOS_MK
