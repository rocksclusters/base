# $Id: Makefile,v 1.3 2010/06/22 21:26:22 mjk Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.3  2010/06/22 21:26:22  mjk
# Build env is now from src/devel package, nothing outside of base roll.
#
# Revision 1.2  2009/11/18 22:16:56  anoop
# - Big changes to rocks-cpan. Now more accurate.
# - CPAN Support introduced. Builds and installs the
#   necessary infrastucture to get CPANPLUS::Dist::Rocks
#   to function correctly
# - Changes to xml files to include CPAN packages and support
#   infrastructure
#
# Revision 1.1  2009/11/10 21:32:28  anoop
# Install CPAN config files to help create RPM files from CPAN directly
# Make sure to build and install rocks-cpan during bootstrap of the base roll
# Include CPAN support on solaris as well. All CPAN files are only for
# foundation-perl
#

REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../devel/devel
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

build:

install::
PKGROOT = `eval "\`$(PERL) -V:privlibexp\`" ; echo $$privlibexp`
SITEROOT = `eval "\`$(PERL) -V:installsitelib\`" ; echo $$installsitelib`
install::
	# Create all the necessary directories
	mkdir -p $(ROOT)/$(PKGROOT)
	mkdir -p $(ROOT)/$(PKGROOT)/CPAN
	mkdir -p $(ROOT)/$(PKGROOT)/CPANPLUS/Config
	mkdir -p $(ROOT)/$(SITEROOT)/CPANPLUS/Dist
	# Install relevant files
	$(INSTALL) -m0544 Config.pm $(ROOT)/$(PKGROOT)/CPAN
	$(INSTALL) -m0544 System.pm $(ROOT)/$(PKGROOT)/CPANPLUS/Config/
	$(INSTALL) -m0544 Rocks.pm $(ROOT)/$(SITEROOT)/CPANPLUS/Dist/
