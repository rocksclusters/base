NAME	= foundation-python
CONFIGOPTS = --enable-ipv6 --enable-unicode=ucs4; 

ifeq ($strip $(VERSION.MAJOR), 5)
VERSION = 2.4.2
RELEASE = 0
ADDFLAGS = 
else
VERSION = 2.6.7
RELEASE = 0
ADDFLAGS = "CFLAGS=-fPIC"
CONFIGOPTS += --exec-prefix=$(PKGROOT)
endif 
