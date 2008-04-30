#
# $Id: Makefile,v 1.3 2007/08/15 18:33:14 bruno Exp $
#
# $Log: Makefile,v $
# Revision 1.3  2007/08/15 18:33:14  bruno
# nuke another spec file
#
#

PKGROOT		= /usr/sbin
REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

CPPFLAGS	= -DVERSION="\"$(VERSION)\""
EXECS		= csp draino detour detach


build: $(EXECS)

csp: csp.o
	$(CC) $(CFLAGS) -o$@ $^

draino: draino.o
	$(CC) $(CFLAGS) -o$@ $^

detour: detour.o
	$(CC) $(CFLAGS) -o$@ $^

detach: detach.o
	$(CC) $(CFLAGS) -o$@ $^


install::
	mkdir -p $(ROOT)/$(PKGROOT)
	$(INSTALL) -m755 $(EXECS) $(ROOT)/$(PKGROOT)


clean::
	-rm -f *.spec
	rm -f *.o $(EXECS)

