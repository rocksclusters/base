#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
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
# Revision 1.4  2008/05/20 02:09:42  anoop
# Made changes to greceptor to make it a bit more usable on Solaris
#
# Revision 1.3  2008/05/20 01:04:29  anoop
# Made Makefiles more Solaris friendly
#
# Revision 1.2  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.1  2008/01/04 23:04:44  bruno
# moved ganglia-pylib and receptor from hpc to base roll
#
# Revision 1.11  2007/06/23 04:03:39  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:48:53  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:10:58  mjk
# 4.2 copyright
#
# Revision 1.8  2006/06/07 04:12:28  bruno
# move over to new build system.
#
# this has the side effect of fixing a problem reported by Noam Bernstein
# where rocks-dist in a cross-kickstart configuration would choose one
# ganglia-receptor*noarch.rpm from either the i386 or the x86_64 hpc roll,
# which would cause greceptor to not work on the non-choosen architecture.
#
# the new build environment removes the 'noarch.rpm' and replaces it with
# the i386.rpm, x86_64.rpm, etc.
#
# Revision 1.7  2005/10/12 18:09:49  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:03:26  mjk
# updated copyright
#
# Revision 1.5  2005/09/02 00:07:40  bruno
# move to foundation
#
# Revision 1.4  2005/08/31 03:05:37  bruno
# included PY.ROCKS
#
# Revision 1.3  2005/08/16 22:04:45  bruno
# move to the foundation
#
# Revision 1.2  2005/05/24 21:22:51  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/12 00:50:26  fds
# Greceptor. Moved from monolithic source tree.
#
# Revision 1.5  2004/07/21 19:57:47  fds
# Make /var/cluster
#
# Revision 1.4  2004/03/25 03:15:04  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.3  2004/02/16 20:13:23  fds
# A small script that will run a ganglia python metric like greceptor.
# Use for cron instead of greceptor.
#
# Revision 1.2  2003/11/05 23:25:31  fds
# Added lock file support for those modules that need it.
#
# Revision 1.1  2003/10/17 19:41:50  fds
# Presenting the greceptor daemon. Replaces gschedule and glisten.
#
#

PKGROOT		= /opt/rocks
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

SCRIPTS		= greceptor grunner
PYLIB		= $(wildcard gmon/*.py)
METRICS		= $(wildcard gmon/metrics/*.py)
LISTENERS	= $(wildcard gmon/listeners/*.py)


build:	$(SCRIPTS)
	

install::
	mkdir -p $(ROOT)/$(PKGROOT)/bin/
	$(INSTALL) -m0555 $(SCRIPTS)  $(ROOT)/$(PKGROOT)/bin/

	mkdir -p $(ROOT)/$(PY.ROCKS)/gmon/
	$(INSTALL) -m0444 $(PYLIB) $(ROOT)/$(PY.ROCKS)/gmon/

	mkdir -p $(ROOT)/$(PY.ROCKS)/gmon/listeners/
	$(INSTALL) -m0444 $(LISTENERS) $(ROOT)/$(PY.ROCKS)/gmon/listeners/

	mkdir -p $(ROOT)/$(PY.ROCKS)/gmon/metrics/
	$(INSTALL) -m0444 $(METRICS) $(ROOT)/$(PY.ROCKS)/gmon/metrics/

	mkdir -p $(ROOT)/$(INIT_SCRIPTS_DIR)
	$(INSTALL) -m0555 greceptor.init $(ROOT)/$(INIT_SCRIPTS_DIR)/greceptor
	(\
	if [ $(OS) == sunos ]; then	\
	$(INSTALL) -m0555 greceptor.init.sunos $(ROOT)/$(INIT_SCRIPTS_DIR)/greceptor;\
	fi;\
	)

	mkdir -p $(ROOT)/var/lock/greceptor-startup/
	mkdir -p $(ROOT)/var/cluster/


clean::
	rm -f $(SCRIPTS)
	rm -f *.pyc gmon/*.pyc
	rm -f $(NAME).spec.in

