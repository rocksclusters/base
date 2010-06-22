# $Id: Rules-macosx.mk,v 1.1 2010/06/22 21:07:44 mjk Exp $
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
# $Log: Rules-macosx.mk,v $
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.18  2009/05/01 19:06:46  mjk
# chimi con queso
#
# Revision 1.17  2008/10/18 00:55:43  mjk
# copyright 5.1
#
# Revision 1.16  2008/03/06 23:41:29  mjk
# copyright storm on
#
# Revision 1.15  2007/06/19 21:39:53  mjk
# dump-names more complete
#
# Revision 1.14  2007/01/12 22:56:07  mjk
# more 3.8.1 fixes
#
# Revision 1.13  2006/12/02 01:04:53  anoop
# Ridiculously big ass commit.
# Also known as the week after thanksgiving 2006. Or "The day Anoop
# broke Rocks".
#
# Main Changes.
#
# 1. Added a roll-profile.mk file. This is meant as a makefile for building
# the profile rpm containing all the XML files meant for the roll. This is a
# breakaway from the spec.in file method of building the profile RPM.
#
# 2. The variable PWD is now changed to CURDIR. The main reason for this is
# PWD is supplied by the shell. CURDIR is the variable supplied by gmake itself.
# This means we can have a slightly more platform independant way of doing things.
# Also Solaris was failing to set PWD correctly in the source directories, wreaking
# havoc on the location of the BUILD and PKG directories.
#
# Revision 1.12  2006/10/15 06:36:11  mjk
# bio perl on my laptop, look at me I'm a biologist
#
# Revision 1.11  2006/09/07 02:41:08  mjk
# added patch version for 4.2.1
#
# Revision 1.10  2006/08/10 00:09:14  mjk
# 4.2 copyright
#
# Revision 1.9  2006/07/13 00:43:04  nadya
# add MYSQL_LDFLAGS for compiling foundation-mysql
#
# Revision 1.8  2006/07/12 22:14:01  nadya
# add CVS
#
# Revision 1.7  2006/07/10 23:32:36  mjk
# add SVN
#
# Revision 1.6  2006/06/05 21:14:17  mjk
# enable suse building
#
# Revision 1.5  2006/01/16 06:25:16  mjk
# first pass at solaris packages
#
# Revision 1.4  2005/12/31 07:37:31  mjk
# configure fix
#
# Revision 1.3  2005/12/31 03:31:14  mjk
# moved stuff in linux makefile
#
# Revision 1.2  2005/12/31 02:51:35  mjk
# *** empty log message ***
#
# Revision 1.1	2005/12/30 22:25:27  mjk
# *** empty log message ***
#

ifndef __RULES_MACOSX_MK
__RULES_MACOSX_MK = yes

# --------------------------------------------------------------------- #
# OS Dependent Stuff
# --------------------------------------------------------------------- #
USERID = $(shell id -u)
INSTALL = install
SVN = /usr/local/bin/svn
CVS = /usr/bin/cvs
MYSQL_LDFLAGS = ""

PYTHON  = /opt/rocks/bin/python
PERL    = /opt/rocks/bin/perl



# --------------------------------------------------------------------- #
# Build the $(NAME).pkg directory
# --------------------------------------------------------------------- #
ROOT	= $(CURDIR)/$(NAME)-buildroot
PKG	= /Developer/Tools/packagemaker

$(ROOT):
	if [ ! -x $(ROOT) ]; then mkdir -p $(ROOT); fi
	
pkg:: root-check $(ROOT) Description.plist Info.plist build install
	chown -R root:wheel $(ROOT)
	$(PKG) -build -ds -d ./Description.plist -i ./Info.plist \
		-p $(NAME).pkg -f $(ROOT)
	cp $(ROCKSROOT)/etc/packagemanager.pdf \
		$(NAME).pkg/Contents/Resources/background.pdf

clean::
	rm -rf $(ROOT) $(NAME).pkg

# --------------------------------------------------------------------- #
# Provide our our plist for the packagemanager.  This allows us not to
# use the GUI and is what apple recommends for scripted packaging.
# --------------------------------------------------------------------- #
PF = @printf

Description.plist: Makefile
	$(PF) '<?xml version="1.0" encoding="UTF-8"?>\n' > $@
	$(PF) '<!DOCTYPE plist PUBLIC ' >> $@
	$(PF)	'"-//Apple Computer//DTD PLIST 1.0//EN" ' >> $@
	$(PF)	'"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n' >> $@
	$(PF) '<plist version="1.0">\n' >> $@
	$(PF) '<dict>\n' >> $@
	$(PF)	'<key>IFPkgDescriptionVersion</key>\n' >> $@
	$(PF)	'<string>$(VERSION)</string>\n' >> $@
	$(PF)	'<key>IFPkgDescriptionTitle</key>\n' >> $@
	$(PF)	'<string>$(NAME)</string>\n' >> $@
	$(PF) '</dict>\n' >> $@
	$(PF) '</plist>\n' >> $@
	
Info.plist: Makefile
	$(PF) '<?xml version="1.0" encoding="UTF-8"?>' >$@
	$(PF) '<!DOCTYPE plist PUBLIC ' >> $@
	$(PF)	'"-//Apple Computer//DTD PLIST 1.0//EN" ' >> $@
	$(PF)	'"http://www.apple.com/DTDs/PropertyList-1.0.dtd">' >> $@
	$(PF) '<plist version="1.0">' >> $@
	$(PF) '<dict>' >> $@
	$(PF)	'<key>IFPkgFormatVersion</key>' >> $@
	$(PF)	'<real>0.10000000149011612</real>' >> $@ # do not change this
	$(PF)	'<key>CFBundleGetInfoString</key>' >> $@
	$(PF)	'<string>$(NAME)</string>' >> $@
	$(PF)	'<key>CFBundleIdentifier</key>' >> $@
	$(PF)	'<string>com.rocksclusters.$(NAME)</string>' >> $@
	$(PF)	'<key>CFBundleShortVersionString</key>' >> $@
	$(PF)	'<string>$(VERSION)</string>' >> $@
	$(PF)	'<key>IFPkgFlagAllowBackRev</key>' >> $@
	$(PF)	'<true/>' >> $@
	$(PF)	'<key>IFPkgFlagAuthorizationAction</key>' >> $@
	$(PF)	'<string>RootAuthorization</string>' >> $@
	$(PF) '</dict>' >> $@
	$(PF) '</plist>' >> $@

clean::
	rm -f Description.plist Info.plist


# --------------------------------------------------------------------- #
# Copy this file into local build directory
# --------------------------------------------------------------------- #
Rules-macosx.mk: $(wildcard $(ROCKSROOT)/etc/Rules-macosx.mk)
	cp $^ $@

clean::
	-rm Rules-macosx.mk

endif	#__RULES_MACOSX_MK
