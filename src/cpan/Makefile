# $Id: Makefile,v 1.1 2009/11/10 21:32:28 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.1  2009/11/10 21:32:28  anoop
# Install CPAN config files to help create RPM files from CPAN directly
# Make sure to build and install rocks-cpan during bootstrap of the base roll
# Include CPAN support on solaris as well. All CPAN files are only for
# foundation-perl
#

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::
PKGROOT = `$(PERL) -V:privlibexp | sed -e "s/[';]//g" | cut -f2 -d=`
install::
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/$(PKGROOT)/CPAN
	mkdir -p $(ROOT)/$(PKGROOT)/CPANPLUS/Config/
	$(INSTALL) -m0544 Config.pm $(ROOT)/$(PKGROOT)/CPAN
	$(INSTALL) -m0544 System.pm $(ROOT)/$(PKGROOT)/CPANPLUS/Config/
