#
# $Id: Makefile,v 1.9 2009/08/24 14:53:58 bruno Exp $
#
# @COPYRIGHT@
# @COPYRIGHT@
#
# $Log: Makefile,v $
# Revision 1.9  2009/08/24 14:53:58  bruno
# more
#
# Revision 1.8  2006/12/06 00:20:20  anoop
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
# Revision 1.7  2006/12/02 01:04:53  anoop
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
# Revision 1.6  2005/12/30 19:35:25  mjk
# removed some of the specfiles
#
# Revision 1.5  2005/09/02 00:05:48  bruno
# pushing toward 4.1 beta
#
# Revision 1.4  2005/08/24 01:23:10  bruno
# added 'done' command
#
#

REDHAT.ROOT     = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

-include $(ROCKSROOT)/etc/python.mk
include python.mk


build:

install::
	mkdir -p $(ROOT)/$(PY.ROCKS)/BitTorrent

	gunzip -c $(BT_NAME)-$(BT_VERSION).tar.gz | $(TAR) xf -
	( cd $(BT_NAME)-$(BT_VERSION)/$(BT_NAME) && \
					cp *py $(ROOT)/$(PY.ROCKS)/BitTorrent )
	( cd patch-files/$(BT_NAME) && cp *py $(ROOT)/$(PY.ROCKS)/BitTorrent )

	cp rocks.py $(ROOT)/$(PY.ROCKS)/BitTorrent

	mkdir -p $(ROOT)/opt/rocks/bittorrent
	(cd $(BT_NAME)-$(BT_VERSION) && cp *py $(ROOT)/opt/rocks/bittorrent)
	(cd patch-files && cp *py $(ROOT)/opt/rocks/bittorrent)
	cp rocks-*.py $(ROOT)/opt/rocks/bittorrent

	mkdir -p $(ROOT)/etc/rc.d/init.d
	cp init.d/rocks-bittorrent $(ROOT)/etc/rc.d/init.d

clean::
	rm -rf $(BT_NAME)-$(BT_VERSION)
	rm -f $(NAME).spec.in

