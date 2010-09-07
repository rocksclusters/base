# $Id: Makefile,v 1.7 2010/09/07 23:52:48 bruno Exp $
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
# Revision 1.7  2010/09/07 23:52:48  bruno
# star power for gb
#
# Revision 1.6  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.5  2009/05/01 19:06:49  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.3  2008/05/20 01:04:29  anoop
# Made Makefiles more Solaris friendly
#
# Revision 1.2  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.1  2007/12/10 21:28:33  bruno
# the base roll now contains several elements from the HPC roll, thus
# making the HPC roll optional.
#
# this also includes changes to help build and configure VMs for V.
#
# Revision 1.11  2007/06/23 04:03:38  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:48:46  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:10:52  mjk
# 4.2 copyright
#
# Revision 1.8  2005/10/12 18:09:41  mjk
# final copyright for 4.1
#
# Revision 1.7  2005/09/16 01:03:18  mjk
# updated copyright
#
# Revision 1.6  2005/09/02 00:08:35  bruno
# move to foundation
#
# Revision 1.5  2005/08/24 20:20:21  bruno
# move more over to the foundation
#
# Revision 1.4  2005/08/08 17:14:37  bruno
# update to rocks foundation
#
# Revision 1.3  2005/05/24 21:22:44  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/04/18 20:08:32  fds
# Allow a frontend to use its 411get to retrieve files from a root server.
#
# Revision 1.1  2005/03/01 02:02:39  mjk
# moved from core to base
#
# Revision 1.20  2004/06/03 17:36:31  fds
# Support for signed messages, and allow different message headers.
#
# Revision 1.19  2004/05/27 01:56:30  fds
# Tweaks
#
# Revision 1.18  2004/04/30 20:35:17  fds
# No blocking for login files at startup.
#
# Revision 1.17  2004/04/13 20:09:30  fds
# Can set polling interval in config file.
#
# Revision 1.16  2004/03/25 03:15:09  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.15  2003/11/26 14:03:38  fds
# Even easier to add files to the 411 service.
# Just append to Files.mk
#
# Revision 1.14  2003/11/05 23:25:05  fds
# Added lock file and new initscript to wait for login files.
#
# Revision 1.13  2003/09/12 21:43:43  fds
# Cleaning up a bit
#
# Revision 1.12  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.11  2003/08/13 19:11:31  fds
# Added var/Makefile like NIS.
#
# Revision 1.10  2003/08/06 00:01:00  fds
# Moved 411 bootstrap service from rocks/config package.
#
# Revision 1.9  2003/07/28 19:06:49  fds
# Warning about a serious security hole.
#
# Revision 1.8  2003/07/25 19:48:33  fds
# Can publish multiple files, tighter headers.
#
# Revision 1.7  2003/07/25 18:01:34  fds
# Added /etc/411.d and removed debug mode.
#
# Revision 1.6  2003/07/23 18:47:55  fds
# Added 'disable' option to the config file.
#
# Revision 1.5  2003/07/22 22:19:45  fds
# Getting ready for packaging.
#
# Revision 1.4  2003/07/22 03:04:25  fds
# Simplified names
#
# Revision 1.3  2003/07/15 21:31:07  fds
# Moved encrypt() into service411, more concious of Python's
# httplib memory leaks.
#
# Revision 1.2  2003/07/09 18:00:08  fds
# Small changes and updated Makefile
#
# Revision 1.1  2003/07/01 23:19:31  fds
# First design
#
#

SCRIPTS = 411get
PKGROOT = /opt/rocks

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk
-include $(ROCKSROOT)/etc/python.mk
include python.mk

METRICS = $(PY.ROCKS)/gmon/metrics
LISTENERS = $(PY.ROCKS)/gmon/listeners

RCFILES = four11getrc


build: $(SCRIPTS)

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/bin/
	mkdir -p $(ROOT)/$(PKGROOT)/etc/
	mkdir -p $(ROOT)/$(METRICS)
	mkdir -p $(ROOT)/$(LISTENERS)
	mkdir -p $(ROOT)/$(PY.ROCKS)/rocks
	$(INSTALL) -m0555 $(SCRIPTS)  $(ROOT)/$(PKGROOT)/bin/
	$(INSTALL) -m0555 metrics/*.py  $(ROOT)/$(METRICS)
	$(INSTALL) -m0444 listeners/*.py $(ROOT)/$(LISTENERS)
	$(INSTALL) -m0444 rocks/*.py $(ROOT)/$(PY.ROCKS)/rocks
	$(INSTALL) -m0644 $(RCFILES) $(ROOT)/$(PKGROOT)/etc/


clean::
	rm -f $(SCRIPTS)
	rm -f *.pyc gmon/*.pyc

