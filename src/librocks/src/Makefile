# $Id: Makefile,v 1.2 2010/10/19 01:04:01 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.2  2010/10/19 01:04:01  mjk
# *** empty log message ***
#
# Revision 1.1  2010/10/18 17:24:37  mjk
# *** empty log message ***
#

default: librocks.so

CFLAGS += -fPIC

OBJS = utils.o channel_clnt.o channel_svc.o

utils.o: utils.c ../include/utils.h

channel_clnt.c channel_svc.c channel.h: channel.x
	rpcgen $^

librocks.so: $(OBJS)
	$(CC) $(CFLAGS) -shared -o $@ $^
clean:
	-rm *.o *.so
	-rm channel_clnt.c channel_svc.c channel.h



