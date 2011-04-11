# $Id: Makefile,v 1.1 2011/04/11 22:41:49 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: Makefile,v $
# Revision 1.1  2011/04/11 22:41:49  anoop
# RPC service that initiates transfer of shared 411 key
#

SRCDIRS = server client

rpm pkg::
	for i in $(SRCDIRS); do		\
		cp $(CURDIR)/sec_channel.x $$i; \
	done

copyright rpm pkg clean::
	for i in $(SRCDIRS); do		\
		$(MAKE) -C $$i $@;	\
	done

clean::
	for i in $(SRCDIRS); do		\
		rm -rf $(CURDIR)/$$i/sec_channel.x; \
	done
