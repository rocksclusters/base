#
# $Id: Makefile,v 1.22 2012/02/02 16:50:23 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.22  2012/02/02 16:50:23  phil
# Add a preroll:: target so that we can put some files in place before roll starts building.
#
# Revision 1.21  2012/01/23 20:07:18  phil
# Makefile now supports version specific files in include directory.
# Bootstrap.sh adds foundation-python-26
#
# Revision 1.20  2011/07/23 02:30:14  phil
# Viper Copyright
#
# Revision 1.19  2010/09/07 23:52:46  bruno
# star power for gb
#
# Revision 1.18  2010/06/29 21:07:53  bruno
# build fixes
#
# Revision 1.17  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.16  2009/05/01 19:06:47  mjk
# chimi con queso
#
# Revision 1.15  2008/10/18 00:55:44  mjk
# copyright 5.1
#
# Revision 1.14  2008/03/10 17:59:44  bruno
# iron curtain test
#
# Revision 1.13  2008/03/06 23:41:30  mjk
# copyright storm on
#
# Revision 1.12  2007/06/23 04:03:18  mjk
# mars hill copyright
#
# Revision 1.11  2006/12/06 00:20:20  anoop
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
# Revision 1.10  2006/09/11 22:46:56  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:23  mjk
# 4.2 copyright
#
# Revision 1.8  2006/06/19 04:20:17  bruno
# build tweaks
#
# Revision 1.7  2005/10/12 18:08:27  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:02:07  mjk
# updated copyright
#
# Revision 1.5  2005/05/24 21:21:46  mjk
# update copyright, release is not any closer
#
# Revision 1.4  2005/03/25 20:57:18  bruno
# need a known good comps file in order to start the build process
#
# Revision 1.3  2005/03/01 18:47:23  mjk
# backout of last change
#
# Revision 1.2  2005/03/01 18:33:18  mjk
# more agressive clean
#
# Revision 1.1  2005/02/28 23:07:28  mjk
# *** empty log message ***
#
# Revision 1.1  2004/12/01 01:31:55  nadya
# baseline
#

ROLLSROOT = $(CURDIR)/src/devel/devel/src/roll
-include $(ROLLSROOT)/etc/Rolls.mk
include Rolls.mk

default: roll

preroll::
	make -C include-version default


