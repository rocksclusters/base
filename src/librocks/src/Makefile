# $Id: Makefile,v 1.1 2010/10/18 17:24:37 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: Makefile,v $
# Revision 1.1  2010/10/18 17:24:37  mjk
# *** empty log message ***
#

default: librocks.so

OBJS = utils.o

utils.o: utils.c ../include/utils.h

librocks.so: $(OBJS)
	$(CC) $(CFLAGS) -fPIC -shared -o $@ $^
clean:
	-rm *.o *.so



