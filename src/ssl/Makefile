# $Id: Makefile,v 1.15 2010/09/07 23:53:09 bruno Exp $
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
# $Log: Makefile,v $
# Revision 1.15  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.14  2010/06/22 21:26:25  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.13  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.12  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.11  2008/03/06 23:41:46  mjk
# copyright storm on
#
# Revision 1.10  2007/06/23 04:03:26  mjk
# mars hill copyright
#
# Revision 1.9  2006/12/06 00:20:22  anoop
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
# Revision 1.8  2006/12/02 01:04:55  anoop
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
# Revision 1.7  2006/09/11 22:47:30  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:09:47  mjk
# 4.2 copyright
#
# Revision 1.5  2005/12/30 19:35:27  mjk
# removed some of the specfiles
#
# Revision 1.4  2005/10/12 18:08:47  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:02:26  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:22:01  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:04:42  mjk
# moved from core to base
#
# Revision 1.20  2004/03/25 03:15:53  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.19  2003/08/15 22:34:47  mjk
# 3.0.0 copyright
#
# Revision 1.18  2003/05/22 16:39:28  mjk
# copyright
#
# Revision 1.17  2003/02/17 18:43:05  bruno
# updated copyright to 2003
#
# Revision 1.16  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.15  2002/10/04 05:33:26  mjk
# more rpm target fixes
#
# Revision 1.14  2002/10/03 23:06:08  mjk
# futzed with CVS repository structure
#
# Revision 1.13  2002/10/03 20:01:43  mjk
# move everything to /opt/rocks
#
# Revision 1.12  2002/02/21 21:33:27  bruno
# added new copyright
#
# Revision 1.11  2001/11/08 18:59:03  mjk
# Bumped version number
#
# Revision 1.10  2001/11/08 18:42:08  mjk
# NPACI Rocks 2.1.1 Release Copyright Notice
#
# Revision 1.9  2001/05/09 20:17:16  bruno
# bumped copyright 2.1
#
# Revision 1.8  2001/04/10 14:16:30  bruno
# updated copyright
#
# Revision 1.7  2001/02/21 04:32:41  mjk
# Docs
#
# Revision 1.6  2001/02/17 03:42:07  mjk
# *** empty log message ***
#
# Revision 1.5  2001/02/16 17:59:59  mjk
# Bump version
# Back to -des
# Fixed typos
#
# Revision 1.4  2001/02/14 20:16:32  mjk
# Release 2.0 Copyright
#
# Revision 1.3  2001/02/14 19:09:44  mjk
# - Don't copy CA Cert over to /var/lib/ssl/certs/ (fixed rexec)
# - Buried some dead code
# - Create the cert dir in the spec file
#
# Revision 1.2  2001/02/14 01:27:35  mjk
# - Lock down key and cert permissions a bit better
# - We still have our pants down since all the keys are unencrypted
#
# Revision 1.1  2001/02/14 01:20:45  mjk
# Initial checkin, actually works!
#


SCRIPTS = ssl-genca ssl-genserver ssl-genuser
OPENSSL = /usr/bin/openssl
PKGROOT = /opt/rocks/
CERTDIR = $(PKGROOT)/lib/

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

SEDSCRIPT += -e s%@CERTDIR@%$(CERTDIR)%g
SEDSCRIPT += -e s%@OPENSSL@%$(OPENSSL)%g

build:

install:: $(SCRIPTS)
	mkdir -p $(ROOT)/$(PKGROOT)/lib/certs
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	$(INSTALL) $(SCRIPTS) $(ROOT)/$(PKGROOT)/sbin/

clean::
	rm -f $(SCRIPTS)
	rm -f $(NAME).spec.in


