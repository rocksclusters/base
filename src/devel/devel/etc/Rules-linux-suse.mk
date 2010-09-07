# $Id: Rules-linux-suse.mk,v 1.2 2010/09/07 23:53:04 bruno Exp $
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
# $Log: Rules-linux-suse.mk,v $
# Revision 1.2  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.12  2009/05/01 19:06:46  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:55:43  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:29  mjk
# copyright storm on
#
# Revision 1.9  2007/10/02 17:31:39  phil
# Add an escape valve RPM.EXTRAS to add odd directives to put in the generated
# spec file.
#
# Revision 1.8  2007/06/19 21:39:53  mjk
# dump-names more complete
#
# Revision 1.7  2007/01/12 22:56:07  mjk
# more 3.8.1 fixes
#
# Revision 1.6  2006/12/02 01:04:53  anoop
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
# Revision 1.5  2006/09/07 02:41:08  mjk
# added patch version for 4.2.1
#
# Revision 1.4  2006/08/10 00:09:14  mjk
# 4.2 copyright
#
# Revision 1.3  2006/07/13 00:43:04  nadya
# add MYSQL_LDFLAGS for compiling foundation-mysql
#
# Revision 1.2  2006/06/24 00:14:48  nadya
# set cvs variable
#
# Revision 1.1  2006/06/05 21:14:17  mjk
# enable suse building
#

ifndef __RULES_LINUX_SUSE_MK
__RULES_LINUX_SUSE_MK = yes

##
## This file is for RedHat/CentOS modify to work on SuSe
##

# --------------------------------------------------------------------- #
# OS Dependent Stuff
# --------------------------------------------------------------------- #
USERID = $(shell id -u)
INSTALL = install
CVS	= /usr/bin/cvs
MYSQL_LDFLAGS = -all-static

# --------------------------------------------------------------------- #
# Copy into /usr/src/redhat (must be done as root)
# Build Package 
# --------------------------------------------------------------------- #

ifeq ($(REDHAT.ROOT),)
REDHAT.ROOT	= /usr/src/redhat
endif
ifeq ($(REDHAT.VAR),)
REDHAT.VAR	= /var
endif

REDHAT.SOURCES	= $(REDHAT.ROOT)/SOURCES
REDHAT.SPECS	= $(REDHAT.ROOT)/SPECS
REDHAT.BUILD	= $(REDHAT.ROOT)/BUILD
REDHAT.RPMS	= $(REDHAT.ROOT)/RPMS
REDHAT.SRPMS	= $(REDHAT.ROOT)/SRPMS

ifeq ($(RPMNAME),)
RPMNAME		:= $(NAME)-$(VERSION)
else
RPMNAME		:= $(RPMNAME)-$(VERSION)
endif


TARBALL		= $(RPMNAME).tar
TARBALL.GZ	= $(TARBALL).gz
SPECFILE	= $(NAME).spec

HOME		= $(CURDIR)

.PHONY: $(HOME)/.rpmmacros
$(HOME)/.rpmmacros:
	rm -f $@
	@echo "%_topdir $(REDHAT.ROOT)" > $@
	@echo "%_var	$(REDHAT.VAR)" >> $@
	@echo "%debug_package	%{nil}" >> $@

clean::
	rm -f $(HOME)/.rpmmacros


.PHONY: pretar
pretar::

$(REDHAT.SOURCES)/$(TARBALL): clean
	$(MAKE) Rules.mk rocks-version.mk pretar 
	if [ `basename $(CURDIR)` = usersguide ]; then $(MAKE) predoc; fi;
	rm -rf $(RPMNAME)
	ln -s . $(RPMNAME)
	tar -cf $@ --exclude $(RPMNAME)/$(RPMNAME) $(TAREXCLUDES) $(RPMNAME)/*
	rm $(RPMNAME)

$(REDHAT.SOURCES)/$(TARBALL.GZ): $(REDHAT.SOURCES)/$(TARBALL)
	gzip -f $^

$(REDHAT.SPECS)/$(SPECFILE): $(SPECFILE)
	$(INSTALL) $^ $@

.PHONY: rpm-mkdirs
rpm-mkdirs:
	if [ ! -x $(REDHAT.SOURCES) ]; then mkdir -p $(REDHAT.SOURCES); fi
	if [ ! -x $(REDHAT.BUILD)  ]; then  mkdir -p $(REDHAT.BUILD); fi
	if [ ! -x $(REDHAT.SPECS) ]; then   mkdir -p $(REDHAT.SPECS); fi
	if [ ! -x $(REDHAT.RPMS) ]; then    mkdir -p $(REDHAT.RPMS); fi
	if [ ! -x $(REDHAT.SRPMS) ]; then   mkdir -p $(REDHAT.SRPMS); fi


ifeq ($(MAKE.rpmflag),)
MAKE.rpmflag = -bb
endif

ifndef MAKE.iscontrib
.PHONY: rpm
rpm:: root-check rpm-mkdirs $(REDHAT.SOURCES)/$(TARBALL.GZ) $(REDHAT.SPECS)/$(SPECFILE) $(HOME)/.rpmmacros
	rpmbuild $(MAKE.rpmflag) $(REDHAT.SPECS)/$(SPECFILE)
else
rpm:: $(HOME)/.rpmmacros
endif

# pkg is an alias for rpm
pkg: rpm

clean::
	rm -f $(REDHAT.SOURCES)/$(TARBALL)
	rm -f $(REDHAT.SOURCES)/$(TARBALL.GZ)


# --------------------------------------------------------------------- #
# Build the spec file keeping the name,version,release in the Makefile 
# --------------------------------------------------------------------- #
PF = printf

ifeq ($(RPM.SUMMARY),)
rpm.summary = Summary: $(NAME)
else
rpm.summart = Summary: $(RPM.SUMMARY)
endif
ifeq ($(RPM.DESCRIPTION),)
rpm.description = $(NAME)
else
rpm.description = $(RPM.DESCRIPTION)
endif
ifneq ($(RPM.PREFIX),)
rpm.prefix = Prefix: $(RPM.PREFIX)
endif
ifneq ($(RPM.ARCH),)
rpm.arch = Buildarch: $(RPM.ARCH)
endif
ifneq ($(RPM.REQUIRES),)
rpm.requires = Requires: $(RPM.REQUIRES)
endif

ifneq ($(shell echo *.spec.in),*.spec.in)
#
# Old Style: Rocks provides a .spec.in file
#
SEDSPEC = \
	-e 's%@PATH.CHILD@%$(PATH.CHILD)%g' \
	-e 's%@PATH.PARENT@%$(PATH.PARENT)%g' \
	-e 's%@NAME@%$(NAME)%g' \
	-e 's%@VERSION@%$(VERSION)%g' \
	-e 's%@RELEASE@%$(RELEASE)%g' \
	-e 's%@COPYRIGHT@%$(COPYRIGHT)%g' \
	-e 's%@VAR@%$(REDHAT.VAR)%g' \
	-e 's%^Vendor:$$%Vendor: $(VENDOR)%g' \
	-e 's%^Prefix:$$%$(rpm.prefix)%g' \
	-e 's%^Buildarch:$$%$(rpm.arch)%g' \
	-e 's%^Requires:$$%$(rpm.requires)%g'

%.spec:%.spec.in
	$(SED) $(SEDSPEC) $^ > $@
else
#
# New Style: Rocks generates the .spec file
#
# The $(NAME).spec.mk file is called by the $(NAME).spec file to
# specify the build and install steps.  This makefile will then
# call make on the main Makefile.  This is done to minimize the
# spec files but more importantly to simplify debugging of RPM
# builds.  The side effect is we can no longer ship SRPMS since the
# spec files refer to developer home directories.  This means tagged
# CVS is the true source for all OSes.
#
$(NAME).spec: $(NAME).spec.mk
	@$(PF) "$(rpm.summary)\n" > $@
	@$(PF) "Name: $(NAME)\n" >> $@
	@$(PF) "Version: $(VERSION)\n" >> $@
	@$(PF) "Release: $(RELEASE)\n" >> $@
	@$(PF) "Copyright: $(COPYRIGHT)\n" >> $@
	@$(PF) "Vendor: $(VENDOR)\n" >> $@
	@$(PF) "Group: System Environment/Base\n" >> $@
	@$(PF) "Source: $(NAME)-$(VERSION).tar.gz\n" >> $@
	@$(PF) "Buildroot: $(shell pwd)/$(NAME).buildroot\n" >> $@
	@$(PF) "$(rpm.prefix)\n" >> $@
	@$(PF) "$(rpm.arch)\n" >> $@
	@$(PF) "$(rpm.requires)\n" >> $@
        echo "$(RPM.EXTRAS)" >> $@
	@$(PF) "%%description\n" >> $@
	@$(PF) "$(rpm.description)\n" >> $@
	@$(PF) "%%prep\n" >> $@
	@$(PF) "%%setup\n" >> $@
	@$(PF) "%%build\n" >> $@
	@$(PF) "$(PF) \"\\\n\\\n\\\n### build ###\\\n\\\n\\\n\"\n" >> $@
	@$(PF) "make -f $(CURDIR)/$(NAME).spec.mk build\n" >> $@
	@$(PF) "%%install\n" >> $@
	@$(PF) "$(PF) \"\\\n\\\n\\\n### install ###\\\n\\\n\\\n\"\n" >> $@
	@$(PF) "make -f $(CURDIR)/$(NAME).spec.mk install\n" >> $@
	@$(PF) "%%files\n" >> $@
	@$(PF) "/\n" >> $@

$(NAME).spec.mk:
	@$(PF) "# This file is called from the generated spec file.\n" > $@
	@$(PF) "# It can also be used to debug rpm building.\n" >> $@
	@$(PF) "# \tmake -f $@ build|install\n" >> $@
	@$(PF) "\n" >> $@
	@$(PF) "ifndef __RULES_MK\n" >> $@
	@$(PF) "\n" >> $@
	@$(PF) "build:\n" >> $@
	@$(PF) "\tmake ROOT=$(shell pwd)/$(NAME).buildroot build\n" >> $@
	@$(PF) "\n" >> $@
	@$(PF) "install:\n" >> $@
	@$(PF) "\tmake ROOT=$(shell pwd)/$(NAME).buildroot install\n" >> $@
	@$(PF) "\n" >> $@
	@$(PF) "endif\n" >> $@

clean::
	rm -rf $(NAME).buildroot
	rm -f  $(NAME).spec.mk
endif

clean::
	rm -f $(NAME).spec

# --------------------------------------------------------------------- #
# Copy this file into the tarball release
# --------------------------------------------------------------------- #
Rules-linux-suse.mk: $(wildcard $(ROCKSROOT)/etc/Rules-linux-suse.mk)
	cp $^ $@

clean::
	-rm Rules-linux-suse.mk

endif	#__RULES_LINUX_SUSE_MK
