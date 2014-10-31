## Create 
DISTRO=CentOS
TSTARCH=$(shell /bin/arch)
ifeq ($(TSTARCH),i686)
ARCH=i386
else
ARCH=$(TSTARCH)
endif

ifeq ($(VERSION.MAJOR), 5)
VERSION=5.9
PKGS=RPMS
BASEPATH=centos/$(VERSION)/os/$(ARCH)/CentOS/
else
VERSION=6.6
PKGS=Packages
BASEPATH=$(VERSION)/os/$(ARCH)/$(PKGS)/
endif

MIRRORURL=http://mirror.pac-12.org
UPDATESPATH=$(VERSION)/updates/$(ARCH)/$(PKGS)/

ROLLNAME=CentOS-$(VERSION)-Updated
