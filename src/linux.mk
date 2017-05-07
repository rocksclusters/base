# $Id: linux.mk,v 1.36 2012/11/27 00:48:01 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
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
# $Log: linux.mk,v $
# Revision 1.36  2012/11/27 00:48:01  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.35  2012/10/23 00:30:04  clem
# foundation-python-xml-26 is not used anywhere...
# We compile it but never install it, let's try to disable its compilation
# and see if it breaks
#
# Revision 1.34  2012/05/06 05:48:13  phil
# Copyright Storm for Mamba
#
# Revision 1.33  2012/04/07 02:59:33  phil
# Build environment-modules for 5
#
# Revision 1.32  2012/01/24 05:07:40  phil
# Add anaconda-yum-plugins for version 6
#
# Revision 1.31  2012/01/23 19:50:59  phil
# On 6, also build anaconda-yum-plugins package
#
# Revision 1.30  2011/12/20 19:19:44  phil
# Remove rebuild of kudzu
#
# Revision 1.29  2011/07/23 02:30:16  phil
# Viper Copyright
#
# Revision 1.28  2011/07/22 23:55:58  anoop
# Finally removed foundation-perl, and CPAN from base roll.
#
# Revision 1.27  2011/04/23 18:36:32  phil
# build devel-env by default
#
# Revision 1.26  2011/04/15 19:41:58  phil
# Updates to build under CentOS 5.6 and new anaconda version.
# Calling this version5.4.3. Codename Viper.
#
# Had to rebuild our own kudzu lib because the CentOS 5.6 version on initial
# release was bad. See bug ID 4813 on bugs.centos.org. That was a not fun debug.
#
# Splash screen is work in progress.
#
# Revision 1.25  2011/04/13 17:45:17  anoop
# Don't build foundation-perl, cpan, & cpan-support when building the
# base roll. This is an ad-hoc solution. Ideally we should move these package
# to their own roll.
#
# Revision 1.24  2010/10/20 21:32:46  mjk
# fix ordering
#
# Revision 1.23  2010/09/20 20:01:54  anoop
# Added lsof to solaris base roll
#
# Revision 1.22  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.21  2010/09/07 23:27:44  bruno
# rocks-bittorrent package is no longer needed. it has been replaced by the
# rocks-tracker package
#
# Revision 1.20  2009/11/23 20:33:41  anoop
# JDK for SunOS in the base roll
#
# Revision 1.19  2009/05/04 21:52:58  bruno
# nuke rocks-security
#
# Revision 1.18  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.17  2009/04/14 16:12:16  bruno
# push towards chimmy beta
#
# Revision 1.16  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.15  2008/05/23 18:59:31  anoop
# Small changes to the base roll to make a cleaner build
#
# Revision 1.14  2008/05/20 01:01:21  anoop
# Added new packages to the base roll. Linux.mk excludes those new packages
# when building the roll on Linux
#
# Revision 1.13  2008/03/06 23:41:31  mjk
# copyright storm on
#
# Revision 1.12  2008/01/04 21:40:53  bruno
# closer to V
#
# Revision 1.11  2007/12/11 00:28:16  bruno
# port to anaconda v11.1.2.87 (the one from RHEL 5 update 1).
#
# Revision 1.10  2007/12/10 21:28:33  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.9  2007/06/23 04:03:19  mjk
# mars hill copyright
#
# Revision 1.8  2007/06/08 19:30:27  anoop
# Build kudzu last, just before anaconda. This removes some ambiguity
# regarding order of package builds.
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
# Revision 1.6  2006/09/11 22:47:01  mjk
# monkey face copyright
#
# Revision 1.5  2006/08/10 00:09:25  mjk
# 4.2 copyright
#
# Revision 1.4  2006/07/19 23:48:47  nadya
# don't build ncurses
#
# Revision 1.3  2006/06/21 14:22:58  bruno
# put firerox back in build process
#
# Revision 1.2  2006/06/05 17:57:34  bruno
# first steps towards 4.2 beta
#
# Revision 1.1  2005/12/31 07:35:46  mjk
# - sed replace the python path
# - added os makefiles
#

-include $(ROCKSROOT)/etc/rocks-version.mk

SRCDIRS = `find . -type d -maxdepth 1 \
	-not -name CVS \
	-not -name . \
	-not -name rocks-pxe \
	-not -name updates.img \
	-not -name anaconda \
	-not -name environment-modules \
	-not -name bittorrent \
	-not -name anaconda-yum-plugins \
	-not -name firerox \
	-not -name foundation-python-xml-26 \
	-not -name developersguiderst \
	-not -name usersguide \
	-not -name channel`

## Build environment modules on 5, it is part of 6 in the OS
ifeq ($(VERSION.MAJOR),5)
SRCDIRS += environment-modules
endif
## 
ifeq ($(VERSION.MAJOR),6)
SRCDIRS += firerox 
endif
#
# make sure we build channel last
#
SRCDIRS += channel 


# For version 6, rebuild anaconda, that's because it includes many packages
# from the base roll. Version 7, we use the native OS version of anaconda
ifeq ($(VERSION.MAJOR), 6)
SRCDIRS += anaconda anaconda-yum-plugins updates.img
endif

