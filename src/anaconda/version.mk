NAME		= anaconda
RELEASE		= 1
MAKE.iscontrib  = 1

ifeq ($(strip $(VERSION.MAJOR)), 5)
VERSION		= 11.1.2.242
SRPMRELEASE	= $(RELEASE)
else
VERSION 	= 13.21.149
SRPMRELEASE	= $(RELEASE).el6
endif

