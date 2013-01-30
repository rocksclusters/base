NAME		= anaconda
RELEASE		= 1
MAKE.iscontrib  = 1

ifeq ($(strip $(VERSION.MAJOR)), 5)
VERSION		= 11.1.2.259
SRPMRELEASE	= $(RELEASE)
else
VERSION 	= 13.21.176
SRPMRELEASE	= $(RELEASE).el6_3
endif

