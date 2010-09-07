# $Id: Makefile,v 1.5 2010/09/07 23:53:04 bruno Exp $

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

# $Log: Makefile,v $
# Revision 1.5  2010/09/07 23:53:04  bruno
# star power for gb
#
# Revision 1.4  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.3  2009/11/20 23:38:38  bruno
# from anoop:
# 	Disable building and installation of rocks-cpan and cpan-support on
# 	Solaris. Will re-enable for next release after testing.
#
# Revision 1.2  2009/11/19 21:10:34  bruno
# patch from anoop
#
# Revision 1.1  2009/11/18 22:16:56  anoop
# - Big changes to rocks-cpan. Now more accurate.
# - CPAN Support introduced. Builds and installs the
#   necessary infrastucture to get CPANPLUS::Dist::Rocks
#   to function correctly
# - Changes to xml files to include CPAN packages and support
#   infrastructure
#

REDHAT.ROOT = $(CURDIR)/../..
ROCKSROOT = ../devel/devel
MAKE.iscontrib = 1
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

# Target to install all the required CPAN modules
# for CPANPLUS::Dist::Rocks to function correctly
# on a vanilla system
bootstrap:
	cat modules.build | while read line; do \
		/opt/rocks/bin/cpan $$line < /dev/null; \
		done

# Make sure we don't build the CPAN modules which are already
# a part of foundation-perl. This is done by creating modules.ignore 
build:
	rpm -q --provides foundation-perl | \
		grep ^perl\( | cut -f1 -d' ' |		\
		sed -e 's/^perl(/^/g' -e 's/)$$/$$/g' |	\
		sort > modules.ignore;			\

# Use modules.build and modules.ignore to convert from CPAN to Rocks RPM
install::
	cp modules.ignore modules.ignore.tmp
	cat modules.build | while read line; do \
		/opt/rocks/bin/cpan2dist --format CPANPLUS::Dist::Rocks \
		--ignorelist modules.ignore.tmp --force --buildprereq	\
		--install --verbose $$line < /dev/null;			\
		( find . -type f -name \*.rpm ! -name \*.src.rpm	\
		  -exec rpm -qp --provides {} \; | grep ^perl\(		\
		  | cut -f1 -d' ' | sed -e 's/^perl(/^/g' -e 's/)$$/$$/g' \
		  && cat modules.ignore ) | sort | uniq > modules.ignore.tmp; \
	done

# Transfer all the RPMS to the Roll RPM  repository.
rpm:: build install
	if [ ! -d $(REDHAT.ROOT)/RPMS ]; then mkdir -p $(REDHAT.ROOT)/RPMS; fi
	for i in `find . -type f -name \*.rpm ! -name \*.src.rpm`; do \
		rpmname=`basename $$i`; \
		arch=`echo $$rpmname | awk -F. '{print $$(NF-1);}'`; \
		echo $$arch; \
		if [ ! -d $(REDHAT.ROOT)/RPMS/$$arch ]; then \
			mkdir -p $(REDHAT.ROOT)/RPMS/$$arch; fi; \
		cp -rvf $$i $(REDHAT.ROOT)/RPMS/$$arch; \
	done

# Clean out everything that's not Makefile or modules.build or CVS
clean::
	find * -prune ! -name CVS ! -name Makefile -a \
		! -name modules.build  -exec rm -rf {} \;
	-rm -rf .gnupg
