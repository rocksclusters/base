# --------------------------------------------------- -*- Makefile -*- --
# $Id: Rules.mk,v 1.7 2012/11/27 00:48:32 phil Exp $
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
# $Log: Rules.mk,v $
# Revision 1.7  2012/11/27 00:48:32  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.6  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.4  2011/02/14 22:14:16  mjk
# - Build Env
#   - ROLLNAME defaults to ROLL
#   - Fixes for docbook
# - All userguides build again
# - All userguides are now NOARCH rpms
#
# Revision 1.3  2011/01/28 02:17:28  mjk
# Docbook cleanup (using Viz Roll as proto-type)
# - consistent entity naming (no more mixing of '-' and '_')
# - roll compat page only lists specified rolls (version.mk)
# - added note about using all OS cds with non-core rolls (e.g. viz)
# - added entities for roll names, and bools
# - logical styles used instead of direct formatting
#   e.g. constant vs. emphasis
# Works for Viz (needs new devel env installed)
# TODO: Update Base Roll to further standardize (slow)
# TODO: Cleanup all other Rolls (fast)
#
# Revision 1.2  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.123  2010/04/13 23:10:59  mjk
# *** empty log message ***
#
# Revision 1.122  2010/04/13 14:51:13  mjk
# rocks is registered
#
# Revision 1.121  2009/07/28 23:17:40  mjk
# Added BLACKOPS support for pulling (cvs co) private stuff from a -blackops
# area into package build directories prior to building.  This is for
# Triton but good for Rocks also.
#
# Revision 1.120  2009/05/01 19:06:46  mjk
# chimi con queso
#
# Revision 1.119  2008/11/03 18:30:13  mjk
# - fix userguide copyright building
# - area51 uses rocks command line
#
# Revision 1.118  2008/10/18 00:55:43  mjk
# copyright 5.1
#
# Revision 1.117  2008/03/06 23:41:29  mjk
# copyright storm on
#
# Revision 1.116  2007/07/25 19:21:47  anoop
# Put the site-specific variables and compiler variables
# at the top of the makefile or atleast above the
# -include Rules-$(OS).mk file
# Otherwise, we cannot override any variables like the CC
# variable in the OS-specific makefiles
#
# Revision 1.115  2007/06/19 21:39:53  mjk
# dump-names more complete
#
# Revision 1.114  2007/06/16 01:40:12  mjk
# - added rocks trademark entities
# - added command line doc building
#
# Revision 1.113  2007/06/12 22:42:00  mjk
# added gpl licenses
#
# Revision 1.112  2007/06/05 22:07:48  bruno
# go from 4.3.0 to 4.3
#
# also fix for two-word release name
#
# Revision 1.111  2007/01/12 22:56:07  mjk
# more 3.8.1 fixes
#
# Revision 1.110  2006/12/02 01:35:19  anoop
# Small changes to the solaris Makefile as well as a really small change to
# Rules.mk file. Now it prints out $(INSTALL) instead of just "install"
# This is to make the code a little more portable.
#
# Revision 1.109  2006/12/02 01:04:53  anoop
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
# Revision 1.108  2006/09/21 04:17:11  mjk
# major doc refresh
#
# Revision 1.107  2006/09/21 01:03:40  mjk
# more doc template changes
#
# Revision 1.106  2006/09/21 00:18:50  mjk
# *** empty log message ***
#
# Revision 1.105  2006/09/15 02:04:55  mjk
# added ROLL_CONFLICTS for docs
#
# Revision 1.104  2006/09/15 00:28:21  mjk
# more docbook rules
#
# Revision 1.103  2006/09/14 21:57:27  mjk
# autocreate entities for all sgml files
#
# Revision 1.102  2006/09/07 02:41:08  mjk
# added patch version for 4.2.1
#
# Revision 1.101  2006/08/15 19:10:48  mjk
# doc additions
#
# Revision 1.100  2006/08/10 00:09:14  mjk
# 4.2 copyright
#
# Revision 1.99  2006/06/21 22:50:35  nadya
# fix NOT syntax
#
# Revision 1.98  2006/01/25 22:22:54  bruno
# compute nodes build again
#
# Revision 1.97  2006/01/21 04:17:30  mjk
# use a _lang file
#
# Revision 1.96  2006/01/21 03:21:09  mjk
# typo
#
# Revision 1.95  2006/01/21 03:20:02  mjk
# typo
#
# Revision 1.94  2006/01/21 03:17:40  mjk
# added _lang file
#
# Revision 1.93  2006/01/18 23:49:25  mjk
# added LANG variable
#
# Revision 1.92  2005/12/31 07:37:02  mjk
# fixed man building
#
# Revision 1.91  2005/12/31 07:01:12  mjk
# *** empty log message ***
#
# Revision 1.90  2005/12/31 07:00:45  mjk
# sed replace the python version
#
# Revision 1.89  2005/12/31 03:31:14  mjk
# moved stuff in linux makefile
#
# Revision 1.88  2005/12/30 22:25:28  mjk
# *** empty log message ***
#
# Revision 1.87  2005/12/30 21:48:20  mjk
# - Can now use os specific makefiles
# - RPM.* macros used to pass info to the template spec file
# - template spec file can handle dependencies, buildarch, and prefixes now.
#   This should let us remove most of our spec files and stop writing
#   new ones.
# - Wrapper tarball (the whole directory) now starts with an '_' this will
#   break some of our hand coded spec files, but the SEDSPEC rules will
#   correct most of this.  Complex spec files will break.
# - arch binary moved to _arch
# - arch _os binary
# - vendor changed from SDSC to Rocks Clusters
#
# Revision 1.86  2005/12/29 18:15:09  mjk
# - Added PY.PATH to find python executable
# - Build the ~/.rpmmacros even for contrib packages
#
# Revision 1.85  2005/10/12 18:08:21  mjk
# final copyright for 4.1
#
# Revision 1.84  2005/09/16 01:02:00  mjk
# updated copyright
#
# Revision 1.83  2005/08/31 03:06:13  bruno
# python variables are in python.mk
#
# Revision 1.82  2005/08/25 18:55:24  mjk
# *** empty log message ***
#
# Revision 1.81  2005/08/25 00:08:19  mjk
# *** empty log message ***
#
# Revision 1.80  2005/07/26 19:49:10  bruno
# added a python version variable for the rocks foundation
#
# Revision 1.79  2005/07/13 01:21:59  mjk
# more foundation changes
#
# Revision 1.78  2005/06/29 22:57:54  mjk
# no more spec files
#
# Revision 1.77  2005/05/27 18:04:33  bruno
# new new home of doc support files
#
# Revision 1.76  2005/05/27 17:51:32  bruno
# move the documentation support files into the roll tree
#
# Revision 1.75  2005/05/24 18:15:42  mjk
# use tarexcludes, faster roll builds
#
# Revision 1.74  2005/04/26 23:27:52  nadya
# add rule to a predoc target where it creates png files
# without the alpha channel. This is a workaround for creating
# pdf docs (pdfjadetex/libpng fail on files with transparency).
#
# Revision 1.73  2005/04/05 20:14:17  nadya
# add predoc target to create rocks.dss, rocks.dsl, and stylesheet-images
# when creating usersguides.
#
# Revision 1.72  2005/03/19 00:43:42  mjk
# build as root, clean as user
#
# Revision 1.71  2005/03/19 00:20:27  mjk
# PATH.PARENT stuff is dead, everything is a roll
#
# Revision 1.70  2005/03/16 19:55:19  fds
# Can change roll name with ROLLNAME
#
# Revision 1.69  2005/02/18 17:21:43  bruno
# right idea, wrong implementation
#
# move the rpm building 'packager' setting to a truly global spot
#
# Revision 1.68  2005/02/18 16:57:27  bruno
# mark all packages built by us
#
# this is useful in determining which packages we need to rebuild after
# rocks-dist has merged all the packages it can find. for example, after
# bootstrapping off a beta, rocks-dist will pick up many binary packages from
# the beta. to make sure we rebuild all non-rocks built packages, we can put
# a check in our 'build-rocks' script to see if the packager is 'Rocks'.
#
# we could have looked at the 'build host', but something tells me that our
# default domain may be changing from sdsc.edu to something that rhymes with
# "pal - guy three - weared".
#
# Revision 1.67  2004/09/10 17:56:51  bruno
# new way (and hopefully easier) to set new rocks version number
#
# Revision 1.66  2004/08/08 17:48:02  najib
# Need a rm -rf to remove a directory which is what RPMNAME seems to be..
#
# Revision 1.65  2004/02/06 20:03:47  fds
# Small
#
# Revision 1.64  2004/01/31 23:43:58  mjk
# support for rolls
#
# Revision 1.63  2004/01/31 19:51:53  mjk
# added time and date stuff
#
# Revision 1.62  2003/11/04 17:51:37  bruno
# drop the .rpmmacros file locally and redirect HOME to it
#
# Revision 1.61  2003/10/14 19:28:47  mjk
# Added rpm-mkdirs target.  This will create the RedHat RPM
# directories (SOURCES, BUILD, etc) in cases where they
# do not exist.  This is useful for building RPMs for Rolls
# without having to a "make roll" first.
#
# Revision 1.60  2003/10/10 04:03:07  bruno
# moved the architecture included file up so we could take more advantage
# of the variable substitution
#
# Revision 1.59  2003/10/08 04:48:41  bruno
# turn off the building of debug packages
#
# Revision 1.58  2003/08/29 22:37:07  mjk
# - Roll tuning
#
# Revision 1.57  2003/08/15 21:07:26  mjk
# - RC files only built one per directory (fixed)
# - Default CGI arch is native (used to be i386)
# - Added scheduler,nameservices to rocksrc.xml
# - insert-ethers know what scheduler and nameservice we use
# - I forget what else
#
# Revision 1.56  2003/08/13 15:24:15  bruno
# made it possible to include a user-defined copyright
#
# Revision 1.55  2003/08/12 20:28:57  mjk
# Add PROJECT_NAME to sed rules
#
# Revision 1.54  2003/07/22 22:32:51  bruno
# move roll directives into etc directory associated with rolls
#
# Revision 1.53  2003/07/19 21:11:42  bruno
# added more stuff to clean
#
# Revision 1.52  2003/07/18 07:05:09  bruno
# now can override NAME
#
# Revision 1.51  2003/07/17 04:56:54  bruno
# moved roll building into rules_mk protection
#
# Revision 1.50  2003/07/12 00:59:28  bruno
# polishing the rolls
#
# Revision 1.49  2003/07/11 14:37:33  bruno
# more roll support
#
# Revision 1.48  2003/07/10 18:23:24  bruno
# moved rollRPMS to bin
#
# Revision 1.47  2003/07/10 18:22:38  bruno
# moved rollRPMS to bin
#
# Revision 1.46  2003/07/08 20:06:03  bruno
# cleanup
#
# Revision 1.45  2003/07/07 16:25:07  mjk
# IA64 redux
#
# Revision 1.44  2003/06/12 23:15:35  bruno
# added ability to get REDHAT.ROOT and REDHAT.VAR
#
# Revision 1.43  2003/02/25 23:00:06  fds
# Recovers from failed rpm builds better.
#
# Revision 1.42  2002/11/01 19:17:06  mjk
# arch binary in all packages
#
# Revision 1.41  2002/10/29 22:42:32  mjk
# moved arch makefile include to the end
#
# Revision 1.40  2002/10/29 22:38:32  mjk
# include .mk makefile
#
# Revision 1.39  2002/10/29 22:35:29  mjk
# added ARCH variable
#
# Revision 1.38  2002/10/18 21:32:28  mjk
# insert-copyright messed this file up
#
# Revision 1.37  2002/10/18 16:32:08  mjk
# added copyright target
#
# Revision 1.36  2002/10/17 20:05:54  mjk
# added pretar hook
#
# Revision 1.35  2002/10/08 22:42:27  mjk
# *** empty log message ***
#
# Revision 1.34  2002/10/06 23:24:03  mjk
# *** empty log message ***
#
# Revision 1.33  2002/10/04 21:02:49  mjk
# USERID check
#
# Revision 1.32  2002/10/04 20:51:10  mjk
# root account changes
#
# Revision 1.31  2002/10/04 18:40:09  mjk
# rocks packages all build now
#
# Revision 1.30  2002/10/04 18:28:47  mjk
# build rpmmacros by default
#
# Revision 1.29  2002/10/04 01:29:11  mjk
# switching to user built rpms
#
# Revision 1.28  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.27  2002/09/25 16:48:10  mjk
# PKGROOT is now used to put everything in /opt/XXXX
#
# Revision 1.26  2002/08/30 15:04:50  bruno
# changed website, ftpsite and bug report to rocksclusters.org
#
# Revision 1.25  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.24  2001/11/02 00:11:40  bruno
# fixed 444 permissions problem on man pages and moved all man pages to
# /usr/share/man
#
# Revision 1.23  2001/10/25 16:19:10  bruno
# updates for local building
#
# Revision 1.22  2001/10/24 20:23:31  mjk
# Big ass commit
#
# Revision 1.21  2001/05/22 20:20:20  bruno
# added mode flag to mkdir -- to make sure the world can read and cd into
# new directories
#
# Revision 1.20  2001/05/09 20:17:09  bruno
# bumped copyright 2.1
#
# Revision 1.19  2001/04/10 14:16:25  bruno
# updated copyright
#
# Revision 1.18  2001/02/21 01:02:13  mjk
# Added clean:: rule for index.html docs
#
# Revision 1.17  2001/02/20 22:42:28  mjk
# Added HTML support for the publish target.  The website documentation
# should be moved into the source code.
#
# Revision 1.16  2001/02/14 20:16:27  mjk
# Release 2.0 Copyright
#
# Revision 1.15  2001/02/13 17:21:40  mjk
# - Added scripts targets
# - Set executable bit on post-processed scripts
#
# Revision 1.14  2001/02/06 18:38:39  mjk
# Added man target
#
# Revision 1.13  2000/12/18 23:40:06  mjk
# Needed to add emtpy targets for manpage-less build directories.
#
# Revision 1.12  2000/11/28 20:46:34  mjk
# Added some manpages, and some minor Rule.mk changes that hit all the
# Makefiles.
#
# Revision 1.11  2000/11/17 00:45:53  mjk
# *** empty log message ***
#
# Revision 1.10  2000/11/16 23:43:12  mjk
# Added a mess of code to make building manpages simpler.
#
# Revision 1.9  2000/11/03 06:11:39  mjk
# Another manpage addition
#
# Revision 1.8  2000/11/03 05:40:46  mjk
# Added man2html rule
#
# Revision 1.7  2000/11/02 04:42:22  mjk
# Added REDHAT_RELEASE for cluster-config RPM
#
# Revision 1.6  2000/11/02 04:22:07  mjk
# Added VENDOR and COPYRIGHT tags for spec.in processing
#
# Revision 1.5  2000/09/18 22:30:20  mjk
# Added Python versioning rule (out from subdirs)
#
# Revision 1.4  2000/09/17 22:54:34  bruno
# build binary and source RPMs -- "-ba" flag
#
# Revision 1.3  2000/07/07 16:27:32  mjk
# Rules.mk added to clean target, this time everything still works
#
# Revision 1.2  2000/07/06 19:11:53  mjk
# Don't clean the Rule.mk file
# Added C, RPCGEN support
#
# Revision 1.1  2000/07/06 18:39:53  mjk
# Extract common stuff into Rules.mk
# Added rpm: target
# Spec file now generated from .spec.in
#
#

ifndef __RULES_MK
__RULES_MK = yes

SHELL = /bin/sh


# --------------------------------------------------------------------- #
# Site specific variables 
# --------------------------------------------------------------------- #
ifeq ($(VENDOR),)
VENDOR    = Rocks Clusters
endif
ifeq ($(COPYRIGHT),)
COPYRIGHT = University of California
endif
ifneq ($(COPYRIGHT.EXTRA),)
COPYRIGHT += / $(COPYRIGHT.EXTRA)
endif
DATE      = $(shell date +"%B %d %Y")
TIME	  = $(shell date +"%T")
TZ	  = $(shell date +"%Z")
PACKAGE   = Rocks
BUGREPORT = info@rocksclusters.org
WEBSITE   = www.rocksclusters.org
FTPSITE   = ftp.rocksclusters.org
MAILTO    = info@rocksclusters.org

# --------------------------------------------------------------------- #
# Compilers
# --------------------------------------------------------------------- #
CC = gcc
CFLAGS    = -g -Wall
CPPFLAGS  = -DVERSION="\"$(VERSION)\""

RPCGEN = rpcgen
RPCGENFLAGS = -C -T

MAN2HTML = man2html
SED = sed

# --------------------------------------------------------------------- #
# Default rule
# --------------------------------------------------------------------- #
default: dump-version dump-name dump-arch


# --------------------------------------------------------------------- #
# Read in the standard makefiles
# --------------------------------------------------------------------- #
-include $(ROCKSROOT)/etc/rocks-version.mk
-include rocks-version.mk
-include $(ROCKSROOT)/etc/python.mk
-include python.mk
-include version.mk

# --------------------------------------------------------------------- #
# Use this target to make sure only the root account is building
# packages.  Some work without but many require root, standardize
# and always require root.
# --------------------------------------------------------------------- #

.PHONY: root-check
root-check:
	@if [ "$(USERID)" != "0" ] ; then \
		echo ; \
		echo ; \
		echo ERROR - YOU MUST BE ROOT TO BUILD PACKAGES; \
		echo ; \
		echo ; \
		exit 1 ; \
	fi

# --------------------------------------------------------------------- #
# Get the absolute path for the root of the sandbox
# --------------------------------------------------------------------- #
ROCKSROOT.ABSOLUTE = $(shell cd $(ROCKSROOT); pwd)

.PHONY: dump-version
dump-version:
	@echo $(VERSION)

# --------------------------------------------------------------------- #
# Compute the package name based on the last two directory names
# --------------------------------------------------------------------- #

PATH.CHILD	= $(notdir $(CURDIR))
PATH.PARENTPATH	= $(dir $(CURDIR))
PATH.PARENTLIST	= $(subst /, ,$(dir $(CURDIR)))
PATH.PARENT	= $(word $(words $(PATH.PARENTLIST)), $(PATH.PARENTLIST))
PATH.GRANDPARENTLIST = $(subst $(PATH.PARENT),,$(PATH.PARENTLIST))
PATH.GRANDPARENT     = $(word $(words $(PATH.GRANDPARENTLIST)), \
	$(PATH.GRANDPARENTLIST))

ifeq ($(NAME),)
NAME		= $(PATH.PARENT)-$(PATH.CHILD)
endif

ifeq ($(ROLL),)
ROLL		= $(PATH.GRANDPARENT)
endif

ifeq ($(ROLLNAME),)
ROLLNAME	= $(ROLL)
endif

.PHONY: dump-name
dump-name:
	@echo $(NAME)
	@echo $(ROLLNAME)
	@echo $(ROLL)

# --------------------------------------------------------------------- #
# Architecture
# --------------------------------------------------------------------- #

ARCH.BIN = $(ROCKSROOT.ABSOLUTE)/bin/arch
ARCH = $(shell if [ ! -x ./_arch ]; then cp $(ARCH.BIN) _arch; fi; ./_arch)

OS.BIN = $(ROCKSROOT.ABSOLUTE)/bin/os
OS = $(shell if [ ! -x ./_os ]; then cp $(OS.BIN) _os; fi; ./_os)

#LANG.BIN = $(ROCKSROOT.ABSOLUTE)/bin/lang
#LANG = $(shell if [ ! -x ./_lang ]; then cp $(LANG.BIN) _lang; fi; ./_lang)


-include $(ARCH).mk
-include $(OS).mk
#-include $(LANG).mk
-include $(ROCKSROOT)/etc/Rules-$(OS).mk
-include Rules-$(OS).mk

ifeq ($(ARCH),x86_64)
LIBARCH = lib64
else
LIBARCH = lib
endif

.PHONY: show-arch
dump-arch:
	@echo $(OS) $(ARCH) $(LIBARCH)

clean::
	-rm -f _arch _os _lang

# --------------------------------------------------------------------- #
# Build man pages and HTML pages
#
# To create a manpage and the html version simple place a file called
# <foo>.<sec>.in in the current directory.  <foo> is the name of the
# manpage, and <sec> is the section name (e.g. 2).  The below rules
# build a makefile that picks up these files and even installs them as
# part of the RPM.
#
# --------------------------------------------------------------------- #

MANSECTIONS = "1 2 3 4 5 6 7 8 l"
MANPATH  = $(ROOT)/$(PKGROOT)/man
HTMLPATH = $(ROOT)/$(PKGROOT)/doc

AWKHTML  = 'BEGIN { state=0; } /<HTML>/ { state=1; } { if (state) { print; }}'

SEDMAN   = \
	-e 's%@PATH.CHILD@%$(PATH.CHILD)%g' \
	-e 's%@PATH.PARENT@%$(PATH.PARENT)%g' \
	-e 's%@NAME@%$(NAME)%g' \
	-e 's%@VERSION@%$(VERSION)%g' \
	-e 's%@RELEASE@%$(RELEASE)%g' \
	-e 's%@COPYRIGHT@%$(COPYRIGHT)%g' \
	-e 's%@DATE@%$(DATE)%g' \
	-e 's%@PACKAGE@%$(PACKAGE)%g' \
	-e 's%@BUGREPORT@%$(BUGREPORT)%g' \
	-e 's%@WEBSITE@%$(WEBSITE)%g' \
	-e 's%@FTPSITE@%$(FTPSITE)%g' \
	-e 's%@MAILTO@%$(MAILTO)%g'

include Rules-install.mk

clean::
	-rm Rules-install.mk

man: $(MANPAGES)

.PHONY: install-man
.PHONY: install-html
install-man::
install-html::

HTMLDOC = $(wildcard *.html.in)
ifneq ($(HTMLDOC),)
%.html: %.html.in
	$(SED) $(SEDMAN) $^ > $@

clean::
	-rm -f $(basename $(HTMLDOC))
endif

Rules-install.mk: Rules.mk Makefile
	@echo $(MANSECTIONS) | awk '\
	BEGIN { \
		RS=" "; FS="\n"; \
		print "#\n# Do not edit\n#\n"; \
	} \
	{ \
		printf "MANPAGES.%s=$$(basename $$(wildcard *.%s.in))\n", \
			$$1, $$1; \
		printf "MANPAGES +=$$(MANPAGES.%s)\n", $$1; \
		printf "\n"; \
		printf "ifneq ($$(MANPAGES.%s),)\n", $$1; \
		printf "HTMLPAGES.%s=$$(addsuffix .html, $$(MANPAGES.%s))\n", \
			$$1, $$1; \
		printf "install-man:: install-man-%s\n", $$1; \
		printf "install-html:: install-html-%s\n", $$1; \
		printf "%%.%s: %%.%s.in\n", $$1, $$1; \
		printf "\t$$(SED) $$(SEDMAN) $$^ > $$@\n"; \
		printf "%%.%s.html: %%.%s\n", $$1, $$1; \
		printf "\t$$(MAN2HTML) $$^ | awk $$(AWKHTML) > $$@\n"; \
		printf "install-man-%s: $$(MANPAGES.%s)\n", $$1, $$1; \
		printf "\tif [ ! -d $$(MANPATH)/man%s ]; then \\\n", $$1; \
		printf "\t\tmkdir -p $$(MANPATH)/man%s; \\\n", $$1; \
		printf "\t\tchmod 755 $$(MANPATH)/man%s; \\\n", $$1; \
		printf "\tfi\n"; \
		printf "\t$$(INSTALL) -ma+r $$^ $$(MANPATH)/man%s\n", $$1; \
		printf "install-html-%s: $$(HTMLPAGES.%s)\n", $$1, $$1; \
		printf "\tif [ ! -d $$(HTMLPATH) ]; then \\\n"; \
		printf "\t\tmkdir $$(HTMLPATH); \\\n"; \
		printf "\t\tchmod 755 $$(HTMLPATH); \\\n"; \
		printf "\tfi\n"; \
		printf "\t$$(INSTALL) -ma+r $$^ $$(HTMLPATH)/\n"; \
		printf "clean::\n"; \
		printf "\trm -f $$(MANPAGES.%s)\n", $$1; \
		printf "\trm -f $$(HTMLPAGES.%s)\n", $$1; \
		printf "docs:: $$(MANPAGES.%s) $$(HTMLPAGES.%s)\n", $$1, $$1; \
		printf "endif\n"; \
		printf "\n"; \
	}' > $@

install:: install-man install-html


# --------------------------------------------------------------------- #
# For Scripts insert the version number
# --------------------------------------------------------------------- #

SCRIPTTYPES = py sh bash csh ksh tcsh pl
SEDSCRIPT = \
	-e s%@NAME@%$(NAME)%g \
	-e s%@VERSION@%$(VERSION)%g \
	-e s%@PROJECT_NAME@%$(PROJECT_NAME)%g \
	-e s%@PYTHON@%$(PY.PATH)%g 

include Rules-scripts.mk

.PHONY: scripts
scripts:: $(SCRIPTS)

clean::
	-rm Rules-scripts.mk

Rules-scripts.mk: Rules.mk Makefile
	@echo $(SCRIPTTYPES) | awk '\
	BEGIN { \
		RS=" "; FS="\n"; \
		print "#\n# Do not edit\n#\n"; \
	} \
	{ \
		printf "%%: %%.%s\n", $$1; \
		printf "\t$$(SED) $$(SEDSCRIPT) $$^ > $$@\n"; \
		printf "\tchmod +x $$@\n"; \
		printf "\n"; \
	}' > $@

# --------------------------------------------------------------------- #
# Build the XML config file
# --------------------------------------------------------------------- #

RCFILES = $(addsuffix rc, $(SCRIPTS))
SEDRC   = $(SEDSCRIPT)

dump-rcfile:
	@echo $(RCFILES)

include Rules-rcfiles.mk

clean::
	-rm Rules-rcfiles.mk

Rules-rcfiles.mk: Rules.mk Makefile
	@echo $(RCFILES) | awk '					\
		BEGIN {							\
			RS=" "; FS="\n";				\
		}							\
		{							\
			printf "%s: %s.xml\n", $$1, $$1;		\
			printf "\t$$(SED) $$(SEDRC) $$^ > $$@\n";	\
		}' > $@



# --------------------------------------------------------------------- #
# Copy this file into the tarball release
# --------------------------------------------------------------------- #
Rules.mk: $(wildcard $(ROCKSROOT)/etc/Rules.mk)
	cp $^ $@

clean::
	rm -f Rules.mk


# --------------------------------------------------------------------- #
# Make a local copy of stylesheets for usersguides
# --------------------------------------------------------------------- #
DOCROOT = $(ROCKSROOT)/src/roll/etc/doc

entities.sgml::
	touch $@
	for sgml in $(basename $(shell ls *.sgml)); do	\
		echo "<!ENTITY source-$$sgml SYSTEM \"$$sgml.sgml\">" >> $@; \
	done
	for roll in $(ROLL_REQUIRES); do \
		echo "<!ENTITY roll-$$roll-depend \"<row><entry namest="req">&roll-$$roll;</entry></row>\">" >> $@; \
	done
	for roll in $(ROLL_CONFLICTS); do \
		echo "<!ENTITY roll-$$roll-depend \"<row><entry namest="con">&roll-$$roll;</entry></row>\">" >> $@; \
	done
ifneq ($(ROLL_REQUIRES_FULL_OS),)
	@echo '<!ENTITY source-roll-overview-complete-os SYSTEM "roll-overview-complete-os.sgml">' >> $@
else
	@echo '<!ENTITY source-roll-overview-complete-os "">' >> $@
endif
	@echo '<!ENTITY document-rollname "$(ROLLNAME)">' >> $@
	@echo '<!ENTITY document-version "$(VERSION)">' >> $@
	@echo '<!ENTITY document-version_name "$(RELEASE_NAME)">' >> $@
	@echo '<!ENTITY document-pubdate "$(PUBDATE)">' >> $@
	@echo '<!ENTITY document-year "$(YEAR)">' >> $@
	@echo '<!ENTITY document-copyright "$(COPYRIGHT)">' >> $@
	@echo '<!ENTITY summary-compatible "$(SUMMARY_COMPATIBLE)">' >> $@
	@echo '<!ENTITY summary-maintainer "$(SUMMARY_MAINTAINER)">' >> $@
	@echo '<!ENTITY summary-architecture "$(SUMMARY_ARCHITECTURE)">' >> $@
	cat $(DOCROOT)/overview-entities.sgml >> $@
	cat $(DOCROOT)/general-entities.sgml >> $@


predoctemplates::
	cp $(DOCROOT)/overview.sgml \
		roll-overview.sgml
	cp $(DOCROOT)/overview-complete-os.sgml \
		roll-overview-complete-os.sgml
	cp $(DOCROOT)/copyright-disclaimer.sgml \
		roll-copyright-disclaimer.sgml
	cp $(DOCROOT)/installing-standard.sgml \
		roll-installing-standard.sgml
	cp $(DOCROOT)/installing-onthefly.sgml \
		roll-installing-onthefly.sgml
	cp $(DOCROOT)/installing-not-onthefly.sgml \
		roll-installing-not-onthefly.sgml
	cp $(DOCROOT)/apachev2-copyright.sgml \
		roll-apachev2-copyright.sgml
	cp $(DOCROOT)/artistic-copyright.sgml \
		roll-artistic-copyright.sgml
	cp $(DOCROOT)/ggplv1-copyright.sgml \
		roll-ggplv1-copyright.sgml
	cp $(DOCROOT)/ggplv2-copyright.sgml \
		roll-ggplv2-copyright.sgml
	cp $(DOCROOT)/glgplv21-copyright.sgml \
		roll-glgplv21-copyright.sgml
	cp $(DOCROOT)/glgplv2-copyright.sgml \
		roll-glgplv2-copyright.sgml
	cp $(DOCROOT)/python2-copyright.sgml \
		roll-python2-copyright.sgml
	cp $(DOCROOT)/rocks-copyright.sgml \
		roll-rocks-copyright.sgml
	cp $(DOCROOT)/images/select-rolls.png \
		images/roll-select-rolls.png
	cp $(DOCROOT)/images/rocks.png \
		images/roll-rocks.png

rcldoc::
	cp $(DOCROOT)/genrcldocs .
	./genrcldocs $(ROLL)

predoc:: predoctemplates rcldoc entities.sgml rocks-copyright.txt
	if [ ! -f ./rocks.dsl ]; then cp $(DOCROOT)/rocks.dsl .; fi; 
	if [ ! -f ./rocks.css ]; then cp $(DOCROOT)/rocks.css .; fi; 
	if [ ! -d ./stylesheet-images ]; then \
           cp -r $(DOCROOT)/stylesheet-images .; \
           rm -rf ./stylesheet-images/CVS ; \
           for i in caution important note tip warning ; do \
               if [ -f ./stylesheet-images/$$i-no-alpha.png ] ; then \
                   cp ./stylesheet-images/$$i-no-alpha.png \
		   ./stylesheet-images/$$i.png ; \
               fi \
           done \
	fi


clean::
	rm -rf rocks.dsl rocks.css stylesheet-images entities.sgml
	rm -f roll-*.sgml
	rm -f images/roll-*.png
	rm -f genrcldocs



# --------------------------------------------------------------------- #
# Blackops support for non-distributable files
# --------------------------------------------------------------------- #


ifneq ($(BLACKOPS),)

BLACKOPS.TAG	= HEAD
BLACKOPS.PATH	= $(BLACKOPS)/src/roll
BLACKOPS.MODULE = $(BLACKOPS.PATH)/$(PATH.GRANDPARENT)/$(PATH.PARENT)/$(PATH.CHILD)

.PHONY: $(BLACKOPS)
$(BLACKOPS):
	if grep @ CVS/Root; then 					\
		cvs export  						\
			-r $(BLACKOPS.TAG) -d $(BLACKOPS) 		\
			$(BLACKOPS.MODULE);				\
	else								\
		cvs -d $(USER)@`cat CVS/Root` export 			\
			-r $(BLACKOPS.TAG) -d $(BLACKOPS)		\
			$(BLACKOPS.MODULE);				\
	fi
	(cd $(BLACKOPS); find . -type f -printf "rm -rf %f\n") > $(BLACKOPS)-clean.sh
	cp -prf $(BLACKOPS)/* .
	rm -rf $(BLACKOPS)

clean::
	if [ -f $(BLACKOPS)-clean.sh ]; then				\
		$(SHELL) $(BLACKOPS)-clean.sh;				\
		rm $(BLACKOPS)-clean.sh;				\
	fi

endif



endif # __RULES_MK

