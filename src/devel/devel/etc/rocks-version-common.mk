#
# $Id: rocks-version-common.mk,v 1.7 2013/01/24 22:13:11 phil Exp $
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
# $Log: rocks-version-common.mk,v $
# Revision 1.7  2013/01/24 22:13:11  phil
# Start the process of building on CentOS 5.9
#
# Revision 1.6  2012/11/27 00:48:32  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.5  2012/07/10 18:40:19  phil
# Update Anaconda for CentOS 6.3.  Add lsscsi and pyparted to os roll inventory
#
# Revision 1.4  2012/05/06 05:48:39  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2012/04/17 07:47:52  phil
# Syntax fix.
#
# Revision 1.2  2012/04/17 03:40:10  phil
# Auto define VERSION.MAJOR based on the OS version.
#
# Revision 1.1  2012/02/01 19:45:03  phil
# Support python 2.4 on 5, 2.6 on 6. Split out the rocks version major, minor and release name to a separate file (rocks-version-common.mk) used by both python.mk and rocks-version.mk
#
#
#

ifndef __ROCKS_VERSION_COMMON_MK
__ROCKS_VERSION_COMMON_MK = yes


# This is included by rocks-version.mk and python.mk
#
# Set these to the major.minor release of rocks and all the RPMS will have 
# the correct version number. 

# The VERSION defaults to the version of Rocks but individual packages
# can override this with their own version numbers.  If you want to
# make sure you get the version of Rocks use ROCKS_VERSION.

ROCKS.OS.VERSION.MAJOR=$(shell lsb_release -rs | cut -d . -f 1)
ifeq ($(strip $(ROCKS.OS.VERSION.MAJOR)), 5)
VERSION.MAJOR = 5
VERSION.MINOR = 6
RELEASE_NAME = Emerald Boa
#VERSION.PATCH = 3
else
VERSION.MAJOR = 6
VERSION.MINOR = 1
VERSION.PATCH = 1
RELEASE_NAME = Sand Boa
endif

VERSION_NAME = "$(RELEASE_NAME)"

rocks-version-common.mk: $(wildcard $(ROCKSROOT)/etc/rocks-version-common.mk)
	cp $^ $@

clean::
	-rm rocks-version-common.mk 

endif
