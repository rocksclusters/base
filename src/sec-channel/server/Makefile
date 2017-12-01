# $Id: Makefile,v 1.6 2012/11/27 00:48:43 phil Exp $

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

# $Log: Makefile,v $
# Revision 1.6  2012/11/27 00:48:43  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.5  2012/08/04 06:34:29  phil
# Have nodes ask to have their secure attributes set as well as the 411 shared
# key.
#
# Revision 1.4  2012/05/06 05:48:48  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:30:50  phil
# Viper Copyright
#
# Revision 1.2  2011/04/20 05:55:04  anoop
# Fixed server to daemonize itself
#
# Revision 1.1  2011/04/11 22:41:50  anoop
# RPC service that initiates transfer of shared 411 key
#

PKGROOT	=	/opt/rocks
REDHAT.ROOT =	$(CURDIR)/../../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

CFLAGS += -DSERVICE_NAME=\"sec_channel_server\"
CFLAGS += -lwrap

sec_channel.h:sec_channel.x
	rpcgen -h -N -o $@ $^
	sed -i sec_channel.h -e 's/sec_channel_ping_1_svc(int/sec_channel_ping_1_svc(int*/'

sec_channel_server: sec_channel_svc.c sec_channel_server.c
	$(CC) $(CFLAGS) -c $^
	$(CC) $(CFLAGS) -o $@ $(^:%c=%o)

build: sec_channel.h sec_channel_server

install::
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	mkdir -p $(ROOT)/$(SCRIPTDEST)
	$(INSTALL) -m0500 sec_channel_server $(ROOT)/$(PKGROOT)/sbin
	$(INSTALL) -m644 $(SCRIPTSRC) $(ROOT)/$(SCRIPTDEST)/$(SCRIPT)

clean::
	rm -rf sec_channel_server	\
	sec_channel.h *.o sec_channel_clnt.c
