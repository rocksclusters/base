# $Id: Makefile,v 1.2 2009/11/19 21:10:34 bruno Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.2  2009/11/19 21:10:34  bruno
# patch from anoop
#
# Revision 1.1  2009/11/18 22:16:56  anoop
# - Big changes to rocks-cpan. Now more accurate.
# - CPAN Support introduced. Builds and installs the
#   necessary infrastucture to get CPANPLUS::Dist::Rocks
#   to function correctly
# - Changes to xml files to include CPAN packages and support
#   infrastructure
#

REDHAT.ROOT = $(CURDIR)/../..
ROCKSROOT   = ../../../../..
MAKE.iscontrib = 1
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

# Target to install all the required CPAN modules
# for CPANPLUS::Dist::Rocks to function correctly
# on a vanilla system
bootstrap:
	cat modules.build | while read line; do \
		/opt/rocks/bin/cpan $$line < /dev/null; \
		done

# Make sure we don't build the CPAN modules which are already
# a part of foundation-perl. This is done by creating modules.ignore 
build:
	rpm -q --provides foundation-perl | \
		grep ^perl\( | cut -f1 -d' ' |		\
		sed -e 's/^perl(/^/g' -e 's/)$$/$$/g' |	\
		sort > modules.ignore;			\

# Use modules.build and modules.ignore to convert from CPAN to Rocks RPM
install::
	cp modules.ignore modules.ignore.tmp
	cat modules.build | while read line; do \
		/opt/rocks/bin/cpan2dist --format CPANPLUS::Dist::Rocks \
		--ignorelist modules.ignore.tmp --force --buildprereq	\
		--install --verbose $$line < /dev/null;			\
		( find . -type f -name \*.rpm ! -name \*.src.rpm	\
		  -exec rpm -qp --provides {} \; | grep ^perl\(		\
		  | cut -f1 -d' ' | sed -e 's/^perl(/^/g' -e 's/)$$/$$/g' \
		  && cat modules.ignore ) | sort | uniq > modules.ignore.tmp; \
	done

# Transfer all the RPMS to the Roll RPM  repository.
rpm:: build install
	if [ ! -d $(REDHAT.ROOT)/RPMS ]; then mkdir -p $(REDHAT.ROOT)/RPMS; fi
	for i in `find . -type f -name \*.rpm ! -name \*.src.rpm`; do \
		rpmname=`basename $$i`; \
		arch=`echo $$rpmname | awk -F. '{print $$(NF-1);}'`; \
		echo $$arch; \
		if [ ! -d $(REDHAT.ROOT)/RPMS/$$arch ]; then \
			mkdir -p $(REDHAT.ROOT)/RPMS/$$arch; fi; \
		cp -rvf $$i $(REDHAT.ROOT)/RPMS/$$arch; \
	done
	
# Clean out everything that's not Makefile or modules.build
clean::
	find * -prune ! -name Makefile -a \
		! -name modules.build  -exec rm -rf {} \;
