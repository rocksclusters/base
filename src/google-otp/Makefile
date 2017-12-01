# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.6 2012/11/27 00:48:37 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# Revision 1.6  2012/11/27 00:48:37  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.5  2012/10/18 17:55:21  phil
# 411 plugin for google authenticator.  creates a tar file of all keys (except
# root) and transfers to login appliances
#
# Revision 1.4  2012/10/18 05:23:13  phil
# missing 's' on plugin directory location
#
# Revision 1.3  2012/10/16 21:18:51  phil
# Patch google-authenticator to not print out the google charts URL. This
# keeps users from making a mistake and transmitting their seeding password in the
# open.
#
# Revision 1.2  2012/09/08 06:24:49  phil
# sync users plugin to add root/users to google-otp group based on
# Info_GoogleOTPUsers and Info_GoogleOTPRoot attributes
#
# Revision 1.1  2012/09/08 01:18:19  phil
# First steps to add google-based OTP (two-factor) authentication.
# Needs plugin for rocks sync users and update to 411 group file to optionally push out OTP secrets to login nodes.
#
#
#

REDHAT.ROOT	= $(CURDIR)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk
ifeq ($(ARCH), x86_64)
PAMLIBDIR=lib64/security
else
PAMLIBDIR=lib/security
endif
PLUGINDIR=$(PY.ROCKS)/rocks/commands/sync/users
PLUGINDIR_411 = /opt/rocks/var/plugins/411




install::
	mkdir -p $(ROOT)/$(PAMLIBDIR)
	mkdir -p $(ROOT)/usr/bin
	mkdir -p $(ROOT)/etc/pam.d
	mkdir -p $(ROOT)/export/google-authenticator
	mkdir -p $(ROOT)/$(PLUGINDIR)
	mkdir -p $(ROOT)/$(PLUGINDIR_411)
	$(INSTALL) -m755 $(NAME)/libpam/pam_google_authenticator.so  $(ROOT)/$(PAMLIBDIR)
	$(INSTALL) -m755 $(NAME)/libpam/google-authenticator $(ROOT)/usr/bin
	$(INSTALL) -m644 google-otp $(ROOT)/etc/pam.d
	$(INSTALL) -m644 plugin_googleotp.py $(ROOT)/$(PLUGINDIR)
	$(INSTALL) -m644 googleotp_411.py $(ROOT)/$(PLUGINDIR_411)
	touch $(ROOT)/export/google-authenticator/keys.tar
	chmod 600 $(ROOT)/export/google-authenticator/keys.tar

build:
	gunzip -c $(NAME).$(VERSION).gz | $(TAR) -xf -
	(cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../)
	(cd $(NAME)/libpam; make)

foo:
	echo $(ARCH)
	echo $(PAMLIBDIR)
clean::
	rm -rf $(NAME) 
