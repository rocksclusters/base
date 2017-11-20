NAME     = roll-$(ROLL)-usersguide
RELEASE  = 2
RPM.ARCH = noarch

SUMMARY_COMPATIBLE      = $(VERSION)
SUMMARY_MAINTAINER      = Rocks Group
SUMMARY_ARCHITECTURE    = x86_64

ifeq ($(VERSION.MAJOR),6)
ROLL_REQUIRES           = kernel base os
else
ROLL_REQUIRES           = kernel core base CentOS 
endif
ROLL_CONFLICTS          =
RPM.FILES	= /var/www/html/roll-documentation/base/*
