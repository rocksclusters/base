# $Id: Rules-linux-centos.mk,v 1.11 2012/11/27 00:48:32 phil Exp $
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
# $Log: Rules-linux-centos.mk,v $
# Revision 1.11  2012/11/27 00:48:32  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.10  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.9  2012/02/01 19:45:03  phil
# Support python 2.4 on 5, 2.6 on 6. Split out the rocks version major, minor and release name to a separate file (rocks-version-common.mk) used by both python.mk and rocks-version.mk
#
# Revision 1.8  2012/01/23 19:57:50  phil
# Updates for rpm version 4
# Set Rocks version to 6.0
# XXX -- Version should really be set from a bootstrap build to we can easily
# flip between 5 and 6 builds. editing rocks-version.mk is cumbersome
#
# Revision 1.7  2011/07/28 21:38:00  phil
# Allow us to specify RPM.FILESLIST as a list of files for rpm to package.
# This is allows us to have RPMS with files, but not owning upper directories.
#
# Revision 1.6  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.5  2011/06/02 02:30:32  phil
# Fix.
#
# Revision 1.4  2011/06/02 01:51:57  phil
# allow multiline EXTRAS
#
# Revision 1.3  2011/03/26 05:33:17  phil
# Enable RPM.FILES.EXTRAS similar RPM.EXTRAS. Use this to define config
# files in the rpm way.
#
# Revision 1.2  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.24  2009/07/28 20:25:14  mjk
# - Remove some dead code
# - User can provide a LICENSE and DESCRIPTION file for the RPM header
#
# Revision 1.23  2009/05/01 19:06:46  mjk
# chimi con queso
#
# Revision 1.22  2008/12/18 17:21:52  mjk
# - For relocatable rpms use the prefix and not / in the spec files section
# - This is for the profiles rpms, might break others (if any exists)
# - I'm an idiot for not seeing the obvious fix
#
# Revision 1.21  2008/11/30 19:20:54  anoop
# Added MPIROOT variable
#
# Revision 1.20  2008/10/18 00:55:43  mjk
# copyright 5.1
#
# Revision 1.19  2008/06/04 00:04:14  bruno
# added support for including a 'BUILDROOT' in version.mk.
#
# this is good for SRPMS that are built on installing nodes (like the pvfs2
# device driver).
#
# Revision 1.18  2008/05/23 19:10:29  anoop
# Removed MYSQL_LDFLAGS from the main Rules file. It really needs
# to belong to some makefile inside the package source directory.
# Also, the flag -all-static breaks the build, and renders gcc unable
# to compile mysql
#
# Revision 1.17  2008/04/28 20:42:38  bruno
# for contrib packages, make sure root builds the packages and that the
# the rpm build directories (e.g., BUILD, RPMS, etc.) are in place
#
# Revision 1.16  2008/03/06 23:41:28  mjk
# copyright storm on
#
# Revision 1.15  2007/12/03 19:54:25  bruno
# 'copyright' is now 'license'
#
# Revision 1.14  2007/10/02 17:31:39  phil
# Add an escape valve RPM.EXTRAS to add odd directives to put in the generated
# spec file.
#
# Revision 1.13  2007/06/19 21:39:53  mjk
# dump-names more complete
#
# Revision 1.12  2007/06/06 18:23:18  anoop
# It's INIT_SCRIPTS_DIR, not INIT_SCRIPT_DIR.
#
# Revision 1.11  2007/04/28 00:28:27  anoop
# *** empty log message ***
#
# Revision 1.10  2007/01/12 22:56:07  mjk
# more 3.8.1 fixes
#
# Revision 1.9  2006/12/06 00:15:25  anoop
# Added two new variables
# TAR
# INIT_SCRIPTS_DIR
#
# They represent the tar executable and the directory for init scripts respectively
#
# Revision 1.8  2006/12/05 19:06:41  anoop
# Now the package format is abstracted. The new variable TARGET_PKG holds
# the package format,ie. RPM in the case of Linux and "pkg" in the case of
# Solaris. This makes the Rolls.mk file a little more simplified
# and more portable.
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
# Revision 1.6  2006/09/07 02:41:08  mjk
# added patch version for 4.2.1
#
# Revision 1.5  2006/08/10 00:09:14  mjk
# 4.2 copyright
#
# Revision 1.4  2006/07/13 00:43:04  nadya
# add MYSQL_LDFLAGS for compiling foundation-mysql
#
# Revision 1.3  2006/07/05 23:08:40  mjk
# fix make roll target
#
# Revision 1.2  2006/06/24 00:14:48  nadya
# set cvs variable
#
# Revision 1.1  2006/06/05 21:14:17  mjk
# enable suse building
#

ifndef __RULES_LINUX_CENTOS_MK
__RULES_LINUX_CENTOS_MK = yes

# --------------------------------------------------------------------- #
# OS Dependent Stuff
# --------------------------------------------------------------------- #
USERID = $(shell id -u)
INSTALL = install
CVS	= /usr/bin/cvs
#MYSQL_LDFLAGS = -all-static
TARGET_PKG = rpm
TAR = tar
INIT_SCRIPTS_DIR = /etc/rc.d/init.d
PROFILE_DIR = /export/profile
MPIROOT	= /opt/openmpi
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
	@echo "%_buildrootdir $(BUILDROOT)" >> $@
	@echo "%buildroot $(BUILDROOT)" >> $@
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
	@echo
	@echo "::: rpm-mkdirs :::"
	@echo
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
rpm:: root-check rpm-mkdirs $(HOME)/.rpmmacros
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

ifdef __ROLLS_MK
RPM.PACKAGE = kickstart
RPM.ARCH = noarch
RPM.SUMMARY = $(ROLLNAME) roll
RPM.DESCRIPTION = XML files for the $(ROLLNAME) roll
RPM.PREFIX = $(PROFILE_DIR)
endif

ifeq ($(RPM.SUMMARY),)
rpm.summary = Summary: $(NAME)
else
rpm.summary = Summary: $(RPM.SUMMARY)
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
oldstylespecfiles = 1
endif

ifdef MAKEPRESPEC
oldstylespecfiles = 1
endif

ifdef oldstylespecfiles
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


.PHONY: prespec
prespec::

%.spec:  %.spec.in
	make prespec
	$(SED) $(SEDSPEC) $^ > $@

$(NAME).spec:  $(NAME).spec.in
	make prespec
	$(SED) $(SEDSPEC) $^ > $@

$(NAME).spec.in:
	cp $(ROLLSROOT)/etc/roll.spec.in $@
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
ifneq ($(RPM.BUILDROOT),)
BUILDROOT = $(RPM.BUILDROOT)
else
BUILDROOT = $(shell pwd)/$(NAME).buildroot
endif

$(NAME).spec: $(NAME).spec.mk
	$(PF) "$(rpm.summary)\n" > $@
	$(PF) "Name: $(NAME)\n" >> $@
	$(PF) "Version: $(VERSION)\n" >> $@
	$(PF) "Release: $(RELEASE)\n" >> $@
	$(PF) "License: " >>$@
	if [ ! -f LICENSE ]; then			\
		$(PF) "$(COPYRIGHT)\n" >> $@;		\
	else						\
		cat LICENSE >> $@;			\
	fi
	$(PF) "Vendor: $(VENDOR)\n" >> $@
	$(PF) "Group: System Environment/Base\n" >> $@
	$(PF) "Source: $(NAME)-$(VERSION).tar.gz\n" >> $@
	$(PF) "Buildroot: $(BUILDROOT)\n" >> $@
	$(PF) "$(rpm.prefix)\n" >> $@
	$(PF) "$(rpm.arch)\n" >> $@
	$(PF) "$(rpm.requires)\n" >> $@
	echo -e "$(RPM.EXTRAS)" >> $@
	$(PF) "%%description\n" >> $@
	if [ ! -f DESCRIPTION ]; then			\
		$(PF) "$(rpm.description)\n" >> $@;	\
	else						\
		cat DESCRIPTION >> $@;			\
	fi
	if [ ! -z $(RPM.PACKAGE) ]; then \
	echo "" >> $@; \
	echo "%package $(RPM.PACKAGE)" >> $@; \
	echo "$(rpm.summary)" >> $@; \
	echo "Group: System Environment/Base" >> $@; \
	echo "%description $(RPM.PACKAGE)" >> $@; \
	echo "$(rpm.description)" >> $@; \
	fi
	@$(PF) "%%prep\n" >> $@
	@$(PF) "%%setup\n" >> $@
	@$(PF) "%%build\n" >> $@
	@$(PF) "$(PF) \"\\\n\\\n\\\n### build ###\\\n\\\n\\\n\"\n" >> $@
	if [ -z "$(RPM.BUILDROOT)" ]; then \
	echo "BUILDROOT=$(BUILDROOT) make -f $(CURDIR)/$(NAME).spec.mk build" >> $@; \
	else \
	echo "BUILDROOT=$(BUILDROOT) make build" >> $@; \
	fi
	@$(PF) "%%install\n" >> $@
	@$(PF) "$(PF) \"\\\n\\\n\\\n### install ###\\\n\\\n\\\n\"\n" >> $@
	if [ -z "$(RPM.BUILDROOT)" ]; then \
	echo "BUILDROOT=$(BUILDROOT) make -f $(CURDIR)/$(NAME).spec.mk install" >> $@; \
	else \
	echo "BUILDROOT=$(BUILDROOT) make install" >> $@; \
	fi
ifeq ($(RPM.FILESLIST),)
	@$(PF) "%%files $(RPM.PACKAGE)\n" >> $@
ifeq ($(RPM.PREFIX),)
	@$(PF) "/\n" >> $@
else
	@$(PF) "$(RPM.PREFIX)\n" >> $@
endif
	echo -e "$(RPM.FILE.EXTRAS)" >> $@
else	
	@$(PF) "%%files $(RPM.PACKAGE) -f $(RPM.FILESLIST)\n" >> $@
endif

$(NAME).spec.mk:
	@$(PF) "# This file is called from the generated spec file.\n" > $@
	@$(PF) "# It can also be used to debug rpm building.\n" >> $@
	@$(PF) "# \tmake -f $@ build|install\n" >> $@
	@$(PF) "\n" >> $@
	@$(PF) "ifndef __RULES_MK\n" >> $@
	@$(PF) "build:\n" >> $@
	@$(PF) "\tmake ROOT=$(shell pwd)/$(NAME).buildroot build\n" >> $@
	@$(PF) "\n" >> $@
	@$(PF) "install:\n" >> $@
	@$(PF) "\tmake ROOT=$(shell pwd)/$(NAME).buildroot install\n" >> $@
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
Rules-linux-centos.mk: $(wildcard $(ROCKSROOT)/etc/Rules-linux-centos.mk)
	cp $^ $@

clean::
	-rm Rules-linux-centos.mk

endif	#__RULES_LINUX_CENTOS_MK
