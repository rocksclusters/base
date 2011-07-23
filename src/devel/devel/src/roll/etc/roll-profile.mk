# $Id: roll-profile.mk,v 1.4 2011/07/23 02:30:43 phil Exp $
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
# $Log: roll-profile.mk,v $
# Revision 1.4  2011/07/23 02:30:43  phil
# Viper Copyright
#
# Revision 1.3  2010/09/28 18:12:55  mjk
# In addition to adding the roll=ROLLNAME attribute in the XML node and graph
# files we now wrap the inside of the <changelogs> as CDATA.  This means we
# can check in XML entities and '<' inside the CVS log.
#
# This is only done for Rolls, which means things like site-profile have
# to manually do this.  But, all the installed nodes/graphs will have it so
# people copying our stuff will do the right thing.
#
# Revision 1.2  2010/09/07 23:53:05  bruno
# star power for gb
#
# Revision 1.1  2010/06/22 21:07:44  mjk
# build env moving into base roll
#
# Revision 1.17  2009/06/16 22:09:43  bruno
# need to include site.attrs in XML nodes rpm (for restore roll)
#
# Revision 1.16  2009/05/01 19:07:15  mjk
# chimi con queso
#
# Revision 1.15  2008/10/18 00:56:07  mjk
# copyright 5.1
#
# Revision 1.14  2008/10/15 20:03:19  mjk
# - ROLLNAME should be defined in the version.mk now
# - Can now build rolls outside of the tree
#
# Revision 1.13  2008/06/27 21:50:14  anoop
# Both jumpstart and kickstart tags are recognized by
# roll-profile.mk
#
# Revision 1.12  2008/04/01 19:40:53  bruno
# put the roll XML file into the roll*kickstart rpm.
#
# this is useful for printing the colors in the dot graph and for re-rolling
# a roll
#
# Revision 1.11  2008/03/06 23:41:50  mjk
# copyright storm on
#
# Revision 1.10  2007/12/06 19:28:26  bruno
# also include 'installclasses' files in the roll-*-kickstart package
#
# Revision 1.9  2007/10/02 23:58:20  anoop
# Remove all references to solaris, and added references to sunos.
# This is to standardize the naming between the python scripts and
# the Makefiles. One less variable that I'll have to deal with.
#
# Revision 1.8  2007/09/04 19:17:21  anoop
# Use "jumpstart" instead of "kickstart" when building on Solaris
#
# Revision 1.7  2007/06/19 21:40:31  mjk
# do not use NAME in roll-profile.mk
#
# Revision 1.6  2007/06/13 16:14:17  bruno
# support for rolls that explicitly name themselves (e.g., with a variable
# definition in version.mk), like the restore roll
#
# Revision 1.5  2007/06/04 22:26:04  mjk
# - Don't delete all files on your system when doing a make clean
#
# Revision 1.4  2007/04/28 00:23:28  anoop
# Modified to accomadate solaris. Now PROFILE_DIR variable is mentioned
# in the top-level os-specific makefile. The reason for this is
# ordinarily /export/profile could be made relocatable. However on Solaris
# relocation of packages don't work in the same way as it does on Linux. So
# PROFILE_DIR needs to be made / on solaris.
#
# Revision 1.3  2007/01/12 22:51:30  mjk
# 3.8.1 fixes
#
# Revision 1.2  2006/12/05 16:12:08  mjk
# fix for insert-copyright
#
# Revision 1.1  2006/12/02 01:04:58  anoop
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
# PWD is supplied by the shell. CURDIR is the variable supplied by gmake 
# itself. This means we can have a slightly more platform independant way of 
# doing things. Also Solaris was failing to set PWD correctly in the source 
# directories, wreaking havoc on the location of the BUILD and PKG directories.
#

node_files := $(wildcard *nodes/*.xml) $(wildcard *nodes/site.attrs)
graph_dir := default
graph_files := $(wildcard graphs/$(graph_dir)/*.xml)
site_nodes := $(wildcard site-nodes/*.xml)
screen_files := $(wildcard include/screens/*.py)
javascript_files := $(wildcard include/javascript/*.js)


ifdef __RULES_LINUX_CENTOS_MK
install_class_files := $(wildcard include/installclass/*.py)
install_classes_files := $(wildcard include/installclasses/*.py)
applet_files := $(wildcard include/applets/*.py)
endif

export PROFILE_DIR

roll-profile.mk:: $(wildcard $(ROLLSROOT)/etc/roll-profile.mk)
	cp $^ $@

$(graph_files)::
	sed \
		-e 's%<graph>%<graph roll="$(ROLLNAME)">%g' \
		-e 's%[[:space:]]*<changelog>%<changelog><![CDATA[%g' \
		-e 's%[[:space:]]*</changelog>%]]></changelog>%g' \
		$@ > $(ROOT)/$(PROFILE_DIR)/$@

# CDATA stuff goes here

$(node_files)::
	sed \
		-e 's%^<kickstart%<kickstart roll="$(ROLLNAME)"%g' \
		-e 's%^<jumpstart%<jumpstart roll="$(ROLLNAME)"%g' \
		-e 's%[[:space:]]*<changelog>%<changelog><![CDATA[%g' \
		-e 's%[[:space:]]*</changelog>%]]></changelog>%g' \
		$@ > $(ROOT)/$(PROFILE_DIR)/$@

$(screen_files) $(install_class_files) $(install_classes_files) $(applet_files) $(javascript_files)::
	$(INSTALL) -m0644 $@ $(ROOT)/$(PROFILE_DIR)/$@

profile_dir::
	mkdir -p $(ROOT)/$(PROFILE_DIR)
	if [ -d graphs/$(graph_dir) ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/graphs/$(graph_dir); ); fi
	if [ -d nodes ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/nodes; ); fi
	if [ -d site-nodes ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/site-nodes; ); fi
	if [ -d include/screens ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/include/screens; ) fi
	if [ -d include/installclass ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/include/installclass; ) fi
	if [ -d include/installclasses ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/include/installclasses; ) fi
	if [ -d include/applets ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/include/applets; ) fi
	if [ -d include/javascript ]; then \
		( mkdir -p $(ROOT)/$(PROFILE_DIR)/include/javascript; ) fi

build: roll-$(ROLLNAME).xml

install:: profile_dir $(node_files) $(graph_files) $(screen_files) $(install_class_files) $(install_classes_files) $(applet_files) $(javascript_files)
	if [ -f roll-$(ROLLNAME).xml ]; then \
		( $(INSTALL) -m0644 roll-$(ROLLNAME).xml \
			$(ROOT)/$(PROFILE_DIR)/ ; ); fi

clean::
	rm -rf roll-profile.mk
