#
# $Id: Makefile,v 1.6 2007/06/14 17:28:42 bruno Exp $
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# $Log: Makefile,v $
# Revision 1.6  2007/06/14 17:28:42  bruno
# cvs.rocksclusters.org doesn't hold the head of the tree
#
# Revision 1.5  2006/12/02 01:04:53  anoop
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
# Revision 1.4  2006/07/26 20:29:18  bruno
# make sure to prune the directories when we check them out
#
# Revision 1.3  2006/07/14 04:45:09  phil
# Add TAG to get specific version of the repository
#
# Revision 1.2  2006/06/24 00:26:09  nadya
# use variable for cvs
#
# Revision 1.1  2005/12/14 21:13:49  bruno
# create an RPM that has:
#
#  - minimum number of files and tree structure in order to build a roll
#  - the 'template' roll (to serve as an example of how to build a roll)
#  - the 'restore' roll (used to backup the important info in your cluster)
#
# Revision 1.1  2005/12/13 04:59:41  bruno
# the start of the 'frontend restore' roll
#
#

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

-include $(ROCKSROOT)/etc/python.mk
include python.mk

CVSROOT = -d bruno@fyp.rocksclusters.org:/home/cvs/CVSROOT
TAG =
# uncomment/change for Release
# TAG = -r ROCKS_4_2


build:
	$(CVS) $(CVSROOT) checkout -P $(TAG) rocks-devel; 
	$(CVS) $(CVSROOT) checkout -P $(TAG) rocks/src/roll/restore
	for i in `find . -type d -name CVS` ; do \
		rm -rf $$i ; \
	done

install::
	mkdir -p $(ROOT)/export/site-roll/
	cp -R rocks $(ROOT)/export/site-roll/

clean::
	rm -f $(NAME).spec.in

