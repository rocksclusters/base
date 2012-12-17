# $Id: Rolls.mk,v 1.8 2012/12/17 21:50:48 clem Exp $
#
# Common Make rules for Rocks rolls.
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
# $Log: Rolls.mk,v $
# Revision 1.8  2012/12/17 21:50:48  clem
# The help target should be defined after the roll target so that make default to roll
#
# When I created the help target I put it above the roll target, since the roll
# makefile does not have a all target it does not define a default, hence make
# picks the first target defined in the makefiles, so I want that to be the "roll"
# target
#
# Revision 1.7  2012/11/27 00:48:34  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.6  2012/10/24 18:25:53  clem
# make help now print some documentation regarding the most usefull built target
#
# Revision 1.5  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.4  2012/02/02 16:50:24  phil
# Add a preroll:: target so that we can put some files in place before roll starts building.
#
# Revision 1.3  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.2  2010/09/07 23:53:05  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.87  2009/05/01 19:07:15  mjk
# chimi con queso
#
# Revision 1.86  2008/10/18 00:56:07  mjk
# copyright 5.1
#
# Revision 1.85  2008/10/15 20:03:19  mjk
# - ROLLNAME should be defined in the version.mk now
# - Can now build rolls outside of the tree
#
# Revision 1.84  2008/08/07 21:19:05  bruno
# fix for building the OS roll
#
# Revision 1.83  2008/03/06 23:41:50  mjk
# copyright storm on
#
# Revision 1.82  2007/10/03 22:32:38  anoop
# More Solaris Support
#
# Revision 1.81  2007/10/02 23:58:20  anoop
# Remove all references to solaris, and added references to sunos.
# This is to standardize the naming between the python scripts and
# the Makefiles. One less variable that I'll have to deal with.
#
# Revision 1.80  2007/07/10 16:23:29  mjk
# use command line instead of rocks-roll
#
# Revision 1.79  2007/06/19 21:40:31  mjk
# do not use NAME in roll-profile.mk
#
# Revision 1.78  2007/06/04 21:55:12  mjk
# - Build Rolls in the background in smp machines
# - Add user and hostname tracking of roll builders to roll xml
#
# Revision 1.77  2007/01/12 22:56:56  mjk
# more 3.8.1 fixes
#
# Revision 1.76  2006/12/05 19:06:41  anoop
# Now the package format is abstracted. The new variable TARGET_PKG holds
# the package format,ie. RPM in the case of Linux and "pkg" in the case of
# Solaris. This makes the Rolls.mk file a little more simplified
# and more portable.
#
# Revision 1.75  2006/12/05 16:05:44  mjk
# forgot the s
#
# Revision 1.74  2006/12/05 08:25:39  mjk
# Can build on Linux again
#
# Revision 1.73  2006/12/02 01:53:02  anoop
# Rolls.mk changed a little bit to accomadate Solaris
#
# bootstrap-functions.sh changed to accomadate solaris. The python code that is
# generated is now a part of install_os_package_linux rather than just install_os_package
#
# Revision 1.72  2006/12/02 01:04:58  anoop
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
# Revision 1.71  2006/09/11 22:48:04  mjk
# monkey face copyright
#
# Revision 1.70  2006/08/10 00:10:20  mjk
# 4.2 copyright
#
# Revision 1.69  2006/01/27 22:29:44  bruno
# stable (mostly) after integration of new foundation and localization code
#
# Revision 1.68  2006/01/17 03:45:27  mjk
# bootstrap works
#
# Revision 1.67  2006/01/17 00:11:37  mjk
# *** empty log message ***
#
# Revision 1.66  2006/01/12 01:02:28  mjk
# *** empty log message ***
#
# Revision 1.65  2006/01/10 16:09:51  mjk
# fixed rm for reroll
#
# Revision 1.64  2006/01/10 16:08:27  mjk
# - Removed dangerous proof target
# - reroll will clean existing iso and disk* first
#
# Revision 1.63  2006/01/10 15:59:58  mjk
# added reroll target for development
#
# Revision 1.62  2005/12/30 21:58:16  mjk
# *** empty log message ***
#
# Revision 1.61  2005/10/12 18:09:08  mjk
# final copyright for 4.1
#
# Revision 1.60  2005/09/16 01:02:44  mjk
# updated copyright
#
# Revision 1.59  2005/08/24 23:30:30  mjk
# *** empty log message ***
#
# Revision 1.58  2005/07/06 20:57:21  mjk
# clean up spec.in file in clean target
#
# Revision 1.57  2005/07/06 20:55:31  mjk
# can build rolls again
#
# Revision 1.56  2005/06/07 18:20:19  mjk
# more precise upload
#
# Revision 1.55  2005/06/07 17:20:47  mjk
# more precise clean of isos
#
# Revision 1.54  2005/06/02 23:46:56  mjk
# *** empty log message ***
#
# Revision 1.53  2005/06/01 19:30:54  mjk
# added compat32 target
#
# Revision 1.52  2005/05/24 23:15:54  fds
# Fixed proof target
#
# Revision 1.51  2005/05/24 17:53:39  bruno
# previous checkin was stupid -- back out
#
# Revision 1.50  2005/05/24 17:52:24  bruno
# only set MKISOFSFLAGS for bootable rolls
#
# Revision 1.49  2005/04/29 01:14:26  mjk
# Get everything in before travel.  Rocks-roll is looking pretty good and
# can now build the os roll (centos with updates).  It looks like only the
# first CDROM of our os/centos roll is needed with 3 extra disks.
#
# - rocks-dist cleanup (tossed a ton of code)
# - rocks-roll growth (added 1/2 a ton of code)
# - bootable rolls do not work
# - meta rolls are untested
# - rocks-dist vs. rocks-roll needs some redesign but fine for 4.0.0
#


ifndef __ROLLS_MK
__ROLLS_MK = yes

# --------------------------------------------------------------------- #
# Initialize some variables for roll building
# --------------------------------------------------------------------- #

ROLLS.API	= 4.0
ROLLS.SERVER	= central-41-devel.rocksclusters.org
ROLLS.PATH	= /export/software/
ROLLS.UPLOAD	= scp

BOOTABLE		= 0
INCLUDE_PROFILES	= 1
INCLUDE_GRAPHS  	= 1
INCLUDE_RPMS		= 1
INCLUDE_SRPMS		= 0
ISOSIZE			= 600

TAREXCLUDES	= --exclude src --exclude BUILD --exclude SOURCES --exclude SPECS --exclude RPMS --exclude SRPMS


# --------------------------------------------------------------------- #
# Include the standard build Rules.mk
# --------------------------------------------------------------------- #

include version.mk

ROCKSROOT = $(ROLLSROOT)/../..

ifeq ($(ROLLNAME),)
ROLLNAME = $(notdir $(CURDIR))
else
NAME     = roll-$(ROLLNAME)
endif
export ROLLNAME
export NAME

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

-include $(ROLLSROOT)/etc/roll-profile.mk
include roll-profile.mk



MKISOFSFLAGS = "-b isolinux/isolinux.bin -c isolinux/boot.cat \
	-no-emul-boot -boot-load-size 4 -boot-info-table"

ifeq ($(ROLLS),)
WITHROLLS = 0
else
WITHROLLS = "$(ROLLS)"
endif


# --------------------------------------------------------------------- #
# support for building rolls
# --------------------------------------------------------------------- #

.PHONY: roll
roll:: preroll $(TARGET_PKG)s profile
	env GNUPGHOME=$(ROCKSROOT.ABSOLUTE)/../.gnupg \
		Kickstart_Lang=$(KICKSTART_LANG) \
		Kickstart_Langsupport=$(KICKSTART_LANGSUPPORT) \
		rocks create roll roll-$(ROLLNAME).xml

.PHONY: reroll
reroll::
	rm -f $(ROLLNAME)-$(VERSION)-$(RELEASE).$(ARCH).disk*.iso 
	rm -rf disk*
	env GNUPGHOME=$(ROCKSROOT.ABSOLUTE)/../.gnupg \
		Kickstart_Lang=$(KICKSTART_LANG) \
		Kickstart_Langsupport=$(KICKSTART_LANGSUPPORT) \
		rocks create roll roll-$(ROLLNAME).xml

upload::
	$(ROLLS.UPLOAD) $(ROLLNAME)-$(VERSION)-$(RELEASE).$(ARCH).disk*.iso $(ROLLS.SERVER):/$(ROLLS.PATH)

pretar:: roll-$(ROLLNAME).xml roll-profile.mk

.PHONY: $(TARGET_PKG)s
$(TARGET_PKG)s: 
	if [ -d src ]; then (cd src; $(MAKE) BG="$(MAKEBG)" $(TARGET_PKG)); fi

.PHONY: profile
profile:: $(TARGET_PKG)-mkdirs
profile::
ifneq ($(INCLUDE_PROFILES),0)
	$(MAKE) MAKE.rpmflag=-bb MAKE.nonuke=1 pkg
endif

.PHONY: preroll 
preroll::

clean::
	rm -f $(ROLLNAME)-$(VERSION)-$(RELEASE).$(ARCH).disk*.iso
	rm -rf disk*
	rm -rf comps 
	rm -f SRPMS/roll-$(ROLLNAME)-$(VERSION)-$(RELEASE).src.rpm
	rm -f RPMS/noarch/roll-$(ROLLNAME)-kickstart-*.noarch.rpm
	if [ -d src ] ; then \
		( cd src ; $(MAKE) BG="$(MAKEBG)" clean ) \
	fi
ifneq ($(MAKE.nonuke),1)
	rm -rf BUILD SOURCES SPECS
endif
ifdef __RULES_SUNOS_MK
	rm -f $(ROLLNAME)-$(VERSION)-$(RELEASE).$(OS).iso
	rm -rf cdrom
	rm -rf PKGS/ROCKSroll-$(ROLLNAME)
endif


# --------------------------------------------------------------------- #
# Some docs of the make target
# --------------------------------------------------------------------- #

help:
	@echo  '  '
	@echo  '  --  Rocks Makefile help  --  '
	@echo  '  '
	@echo  '  '
	@echo  '   - Top directory targets'
	@echo  '     (these target must be run from the top level roll source directory)'
	@echo  '  '
	@echo  '  roll             - This target creates a Rocks Roll from a roll source directory'
	@echo  '                     tree. It will create all the RPM packages, bundle all the .xml '
	@echo  '                     nodes and graphs files, and create the iso. It is the default target.'
	@echo  '                     (to create a source directory tree run "rocks create roll foo")'
	@echo  '  profile          - This target create the roll-<rollname>-kickstart RPM which contains'
	@echo  '                     all the node xml and graph xml files and all the include/ and '
	@echo  '                     include-version/ files. The final RPM is placed under RPMS/noarch'
	@echo  '  reroll           - This target only recreate the ISO image using the already built RPMs'
	@echo  '  '
	@echo  '                     If you only modify the xml file of your roll after the last compilation'
	@echo  '                     you can simply run make profile and then make reroll'
	@echo  '  '
	@echo  '  '
	@echo  '   - Package level directory targets'
	@echo  '     (these targets must be run from the src/<packagename> source directory)'
	@echo  '  '
	@echo  '  rpm              - It can be used to create a single RPM from a specific package '
	@echo  '                     directory. It will create the final RPM inside the ../../RPMS/$(ARCH)'
	@echo  '  '
	@echo  '  '
	@echo  '  '



# --------------------------------------------------------------------- #
# Build the Dot graph
# --------------------------------------------------------------------- #

.PHONY: graph

graph: graph-edges.pdf graph-order.pdf graph-all.pdf

graph-edges.pdf:
	kpp --draw-edges | dot -Tps2 | ps2pdf - $@

graph-order.pdf:
	kpp --draw-order | dot -Tps2 | ps2pdf - $@

graph-all.pdf:
	kpp --draw-all | dot -Tps2 | ps2pdf - $@

clean::
	rm -f graph-*.pdf


# --------------------------------------------------------------------- #
# Build to roll.xml file
# --------------------------------------------------------------------- #

roll-$(ROLLNAME).xml:
	@echo "<roll name=\"$(ROLLNAME)\" interface=\"$(ROLLS.API)\">" > $@
	@echo "	<timestamp time=\"$(TIME)\""\
		"date=\"$(DATE)\" tz=\"$(TZ)\"/>" >> $@	
	@echo "	<color edge=\"$(COLOR)\" node=\"$(COLOR)\"/>" >> $@
	@echo "	<info version=\"$(VERSION)\" release=\"$(RELEASE)\""\
		"arch=\"$(ARCH)\" os=\"$(OS)\"/>" >> $@
	@echo "	<iso maxsize=\"$(ISOSIZE)\" bootable=\"$(BOOTABLE)\""\
		"mkisofs=\"$(MKISOFSFLAGS)\"/>" >> $@
	@echo "	<$(TARGET_PKG) rolls=\"$(WITHROLLS)\""\
		"bin=\"$(INCLUDE_RPMS)\" src=\"$(INCLUDE_SRPMS)\"/>" >> $@
	@echo "	<author name=\"$(USER)\""\
		"host=\"$(shell /bin/hostname)\"/>" >> $@
	@echo "</roll>" >> $@

clean::
	rm -f roll-$(ROLLNAME).xml


# --------------------------------------------------------------------- #
# Copy this file into the tarball release
# --------------------------------------------------------------------- #
Rolls.mk: $(wildcard $(ROLLSROOT)/etc/Rolls.mk)
	cp $^ $@

clean::
	rm -f Rolls.mk 
	rm -rf anaconda anaconda-runtime
	rm -rf rpmdb

endif
