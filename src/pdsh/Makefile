# $Id: Makefile,v 1.4 2012/05/06 05:48:45 phil Exp $
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
# Revision 1.4  2012/05/06 05:48:45  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/08/24 22:22:33  anoop
# Cleanup
#
# Revision 1.2  2011/07/23 02:30:48  phil
# Viper Copyright
#
# Revision 1.1  2011/03/09 03:11:37  phil
# pdsh -- some people asked for it
#
# Revision 1.1  2010/10/01 20:13:20  phil
# Easily set up generic IP tunnels.
#

REDHAT.ROOT = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


build:
	bunzip2 -c $(NAME)-$(VERSION).$(TARBALL_POSTFIX) | $(TAR) -xf -
	( 							\
		cd $(NAME)-$(VERSION);				\
		./configure --prefix=$(PKGROOT)/$(NAME)		\
			--with-ssh --with-readline		\
			--with-fanout=64 --with-timeout=30 	\
			--with-rcmd-rank-list=ssh,exec,rsh ;	\
		$(MAKE);					\
	)
	echo $(PKGROOT)/$(NAME)/lib/$(NAME) > pdsh.conf
	
install::
	mkdir -p $(ROOT)/$(PKGROOT)/$(NAME)
	mkdir -p $(ROOT)/etc/profile.d
	mkdir -p $(ROOT)/etc/ld.so.conf.d
	(							\
		cd $(NAME)-$(VERSION);				\
		$(MAKE) prefix=$(ROOT)/$(PKGROOT)/$(NAME) install;\
	)
	install -m644 pdsh.conf $(ROOT)/etc/ld.so.conf.d
	install -m755 pdsh.sh $(ROOT)/etc/profile.d
	install -m755 pdsh.csh $(ROOT)/etc/profile.d

clean::
	rm -rf $(NAME)-$(VERSION)
