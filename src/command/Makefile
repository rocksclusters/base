# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.24 2012/05/06 05:48:18 phil Exp $
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
# Revision 1.24  2012/05/06 05:48:18  phil
# Copyright Storm for Mamba
#
# Revision 1.23  2012/01/23 19:54:49  phil
# Tweak for new RPM building macros
#
# Revision 1.22  2011/07/23 02:30:24  phil
# Viper Copyright
#
# Revision 1.21  2010/09/07 23:52:49  bruno
# star power for gb
#
# Revision 1.20  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.19  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.18  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.17  2008/03/06 23:41:33  mjk
# copyright storm on
#
# Revision 1.16  2008/03/03 20:21:25  mjk
# kill readline
#
# Revision 1.15  2008/03/03 20:16:53  mjk
# no more command line completion
#
# Revision 1.14  2007/10/02 23:58:20  anoop
# Remove all references to solaris, and added references to sunos.
# This is to standardize the naming between the python scripts and
# the Makefiles. One less variable that I'll have to deal with.
#
# Revision 1.13  2007/09/04 19:07:18  anoop
# Dynamically changes path of the MySQL Socket during building of package
# Does this only on Solaris, and not on Linux.
#
# Revision 1.12  2007/08/14 20:09:40  anoop
# Awk behaves strangely on Solaris. Need gawk instead
#
# Revision 1.11  2007/06/19 16:42:39  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.10  2007/06/18 18:32:00  mjk
# name commands by roll name
#
# Revision 1.9  2007/06/05 18:31:52  mjk
# - Added rocks5 to test command line with foundation-mysql (v5)
# - Same script just uses a different UNIX socket
#
# Revision 1.8  2007/05/25 03:17:50  mjk
# way cool
#
# Revision 1.7  2007/05/25 03:12:30  mjk
# - help takes a flag instead of an argument
# - added bash/readline completion
#
# Revision 1.6  2007/05/08 22:41:37  anoop
# find does not work without a path, on Solaris
#
# Revision 1.5  2006/12/17 20:19:47  mjk
# moving commands around again
#
# Revision 1.4  2006/12/06 00:20:20  anoop
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
# Revision 1.3  2006/12/02 01:04:53  anoop
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
# Revision 1.2  2006/11/22 02:15:46  mjk
# working version
#
# Revision 1.1  2006/11/02 21:49:46  mjk
# prototype
#

SCRIPTS     	= rocks 
PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build: $(SCRIPTS) rocks-copyright.txt

install::
	mkdir -p $(ROOT)/$(PKGROOT)/bin
	mkdir -p $(ROOT)/$(PY.ROCKS)/rocks/commands
	mkdir -p $(ROOT)/etc/profile.d/
	$(INSTALL) -m0555 $(SCRIPTS)  $(ROOT)/$(PKGROOT)/bin/
	(								\
		cd commands;						\
		find . -name "*.py" | 					\
			cpio -pduv $(ROOT)/$(PY.ROCKS)/rocks/commands;	\
	)
	(								\
		if [ $(OS) == 'sunos' ]; then 			\
		sed -e 's/var.lib.mysql/var\/opt\/rocks\/mysql/g' 	\
			$(ROOT)/$(PKGROOT)/bin/rocks > /tmp/rocks.py; 	\
		mv /tmp/rocks.py $(ROOT)/$(PKGROOT)/bin/rocks;		\
		chmod 0555 $(ROOT)/$(PKGROOT)/bin/rocks;		\
		fi ;\
	);
	find $(ROOT)/$(PY.ROCKS)/rocks/commands -name "*.py" | gawk	\
		'{ print "\nRollName = \"$(ROLL)\"" >> $$1; }'  
	$(INSTALL) -m0444 rocks-copyright.txt \
		$(ROOT)/$(PY.ROCKS)/rocks/commands/list/license/license.txt
	find $(ROOT) -type d -exec chmod a+rx {} \;
	#find $(ROOT) | sed "s%$(ROOT)%%" > $(RPM.FILESLIST) 

clean::
	rm -f $(SCRIPTS)
