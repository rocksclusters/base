## Create 
DISTRO=CentOS
ARCH=x86_64
ifeq ($(VERSION.MAJOR), 5)
VERSION=5.7
PKGS=RPMS
BASEPATH=centos/$(VERSION)/os/$(ARCH)/CentOS
else
VERSION=6.2
PKGS=Packages
BASEPATH=centos/$(VERSION)/os/$(ARCH)/$(PKGS)
endif

MIRRORURL=http://mirror.hmc.edu
UPDATESPATH=centos/$(VERSION)/updates/$(ARCH)/$(PKGS)

