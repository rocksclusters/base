#!/bin/bash
#
# This file should remain OS independent
#
# $Id: bootstrap.sh,v 1.18 2009/11/10 21:32:28 anoop Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: bootstrap.sh,v $
# Revision 1.18  2009/11/10 21:32:28  anoop
# Install CPAN config files to help create RPM files from CPAN directly
# Make sure to build and install rocks-cpan during bootstrap of the base roll
# Include CPAN support on solaris as well. All CPAN files are only for
# foundation-perl
#
# Revision 1.17  2009/05/20 01:48:58  anoop
# Add foundation-python-xml to bootstrapping procedure of the base roll
#
# Revision 1.16  2009/05/16 02:16:02  anoop
# Removed out-dated utils from bootstrap process
#
# Revision 1.15  2009/05/15 00:38:11  anoop
# Adding libdnet to the mix
#
# Revision 1.14  2009/05/01 19:06:47  mjk
# chimi con queso
#
# Revision 1.13  2008/10/18 00:55:44  mjk
# copyright 5.1
#
# Revision 1.12  2008/03/06 23:41:30  mjk
# copyright storm on
#
# Revision 1.11  2007/09/04 19:28:39  anoop
# Additional Packages to bootstrap self.
#
# Revision 1.10  2007/06/23 04:03:18  mjk
# mars hill copyright
#
# Revision 1.9  2006/12/06 00:20:20  anoop
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
# Revision 1.8  2006/09/11 22:46:56  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:23  mjk
# 4.2 copyright
#
# Revision 1.6  2006/08/02 21:44:06  mjk
# foundation-perl
#
# Revision 1.5  2006/02/07 22:00:30  mjk
# *** empty log message ***
#
# Revision 1.4  2006/01/19 21:27:11  mjk
# more foundation changes
#
# Revision 1.3  2006/01/18 06:12:41  mjk
# more foundation work
#
# Revision 1.2  2006/01/17 03:45:58  mjk
# might be complete now
#
# Revision 1.1  2006/01/17 00:14:23  mjk
# bootstrap roll development
#

. ../etc/bootstrap-functions.sh

if [ `./_os` == "linux" ]; then
	compile_and_install foundation-redhat
fi
compile_and_install foundation-coreutils
compile_and_install foundation-gawk
compile_and_install foundation-readline
compile_and_install foundation-wget
compile_and_install foundation-mysql
compile_and_install foundation-python
compile_and_install foundation-perl
compile_and_install foundation-libxml2
compile_and_install foundation-python-xml
compile_and_install foundation-python-extras
compile_and_install foundation-rcs

compile pylib
install rocks-pylib

compile command
install rocks-command

compile dnet
install libdnet

compile cpan
install rocks-cpan

if [ `./_os` == "linux" ]; then
	ignore_os_package ntp
	ignore_os_package httpd
	ignore_os_package openssh
	ignore_os_package openssh-clients
	ignore_os_package openssh-server
	ignore_os_package openssh-askpass
	install_os_packages server
fi
