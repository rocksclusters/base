# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.11 2008/10/18 00:56:00 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# Revision 1.11  2008/10/18 00:56:00  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.9  2007/12/10 21:28:34  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.8  2007/10/25 05:32:10  anoop
# Small changes to accommodate solaris
#
# Revision 1.7  2007/09/04 16:19:48  anoop
# Removing numpy and pygtk from the solaris build.
#
# Revision 1.6  2007/06/23 04:03:23  mjk
# mars hill copyright
#
# Revision 1.5  2006/12/02 01:04:54  anoop
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
# Revision 1.4  2006/09/11 22:47:14  mjk
# monkey face copyright
#
# Revision 1.3  2006/08/10 00:09:36  mjk
# 4.2 copyright
#
# Revision 1.2  2006/01/16 23:14:06  mjk
# - more source built foundations
# - scipy stuff is here now (may move to hpc roll)
#
# Revision 1.1  2006/01/16 16:10:52  mjk
# *** empty log message ***
#

PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build::
#	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	
install::
	mkdir -p $(ROOT)/$(PKGROOT)

include MySQL-python.mk Numeric.mk POW.mk \
	PyXML.mk egenix-mx-base.mk libxml2dom.mk \
	numarray.mk pexpect.mk IPy.mk

