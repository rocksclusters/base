## Create 
DISTRO=CentOS
TSTARCH=$(shell /bin/arch)
ifeq ($(TSTARCH),i686)
ARCH=i386
else
ARCH=$(TSTARCH)
endif

ifeq ($(VERSION.MAJOR), 5)
VERSION=5.8
PKGS=RPMS
BASEPATH=centos/$(VERSION)/os/$(ARCH)/CentOS
else
VERSION=6.2
PKGS=Packages
BASEPATH=centos/$(VERSION)/os/$(ARCH)/$(PKGS)
endif

MIRRORURL=http://mirror.hmc.edu
UPDATESPATH=centos/$(VERSION)/updates/$(ARCH)/$(PKGS)

