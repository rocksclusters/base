# $Id: Makefile,v 1.15 2012/11/27 00:48:08 phil Exp $
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
# $Log: Makefile,v $
# Revision 1.15  2012/11/27 00:48:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.14  2012/08/09 23:16:48  clem
# bug fix for the following problem:
#
# Centos 6.* libtirpc-0.2.1 are bugged cannot get return value from the server
# https://bugzilla.redhat.com/show_bug.cgi?format=multiple&id=781880
#
# Revision 1.13  2012/05/06 05:48:18  phil
# Copyright Storm for Mamba
#
# Revision 1.12  2011/07/23 02:30:24  phil
# Viper Copyright
#
# Revision 1.11  2011/01/25 23:20:24  anoop
# hexdump and -Wall are linux only
#
# Revision 1.10  2011/01/25 23:14:40  mjk
# actually builds
#
# Revision 1.8  2011/01/21 20:08:46  anoop
# Solaris build fixes
#
# Revision 1.7  2010/11/28 00:33:16  anoop
# channeld init script is now OS specific
#
# Revision 1.6  2010/11/04 02:20:15  anoop
# Solaris compatibility fixes
#
# Revision 1.5  2010/10/21 00:21:00  bruno
# name the init script 'channeld'
#
# Revision 1.4  2010/10/20 23:44:46  bruno
# tweak
#
# Revision 1.3  2010/10/20 23:41:04  mjk
# forgot to make this into a service
# needs a solaris version as well
#
# Revision 1.2  2010/10/20 21:12:34  mjk
# works
#
# Revision 1.1  2010/10/19 23:06:29  mjk
# c is hard
#


PKGROOT		= /opt/rocks
REDHAT.ROOT	= $(CURDIR)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

CFLAGS		= -g 

ifeq ($(OS), linux)
CFLAGS		+= -Wall 
CPPFLAGS	= -I/opt/rocks/include
LDFLAGS		= -L/opt/rocks/lib -lrocks

ifeq ($(strip $(VERSION.MAJOR)), 6)
#Centos 6.* libtirpc-0.2.1 are bugged cannot get return value from the server
#https://bugzilla.redhat.com/show_bug.cgi?format=multiple&id=781880
CFLAGS          += -DROCKS6
endif
endif

ifeq ($(OS), sunos)
CFLAGS		+= -m64
LDFLAGS		+= -lrpcsvc -lnsl
endif


#	rpcgen -h -N -o channel.h $@

channel_svc.c: channel.x channel.h
	rpcgen -m -N -o $@ $<

channel_clnt.c: channel.x
	rpcgen -l -N -o $@ $<

channel_xdr.c: channel.x channel.h
	rpcgen -c -N -o $@ $<

channel.h: channel.x
	rpcgen -h -N -o $@ $<

server.o: server.c channel.h

411-alert.o: 411-alert.c channel.h

channeld: server.o channel_svc.o channel_xdr.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

411-alert: 411-alert.o channel_xdr.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^


build: channeld 411-alert 411-alert-handler

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/sbin
	mkdir -p $(ROOT)/$(INIT_SCRIPTS_DIR)
	$(INSTALL) -m544 411-alert $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m544 411-alert-handler $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m544 channeld  $(ROOT)/$(PKGROOT)/sbin/
	$(INSTALL) -m755 channel.init.$(OS) $(ROOT)/$(INIT_SCRIPTS_DIR)/channeld

clean::
	-rm *.o
	-rm channeld 411-alert 411-alert-handler
	-rm channel_svc.c channel.h
	-rm channel_clnt.c channel_xdr.c
