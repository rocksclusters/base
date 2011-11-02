## Makefile to create an OS Roll and Updates
## $Id: Makefile,v 1.1 2011/11/02 16:43:38 phil Exp $
## $Log: Makefile,v $
## Revision 1.1  2011/11/02 16:43:38  phil
## In bootstrap0, create an OS and Updates roll after the Rocks database is up and running.
##
include version.mk

default: updates 

# Create the Base OS Roll
base: 
	 /opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(BASEPATH) arch=$(ARCH) rollname=$(DISTRO) version=$(VERSION)
	/sbin/service httpd stop
	/opt/rocks/bin/rocks add roll $(DISTRO)-$(VERSION)-*.iso
	/sbin/service httpd start
	/opt/rocks/bin/rocks enable roll $(DISTRO)

# Mirror Updates, then add to distro
updates: cleanupdates
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(UPDATESPATH) arch=$(ARCH) rollname=Updates-$(DISTRO)-$(VERSION) version="`date +%F`"
	- /sbin/service httpd stop
	/opt/rocks/bin/rocks add roll Updates-$(DISTRO)-$(VERSION)-*.$(ARCH).*.iso
	-/sbin/service httpd start
	/opt/rocks/bin/rocks enable roll Updates-$(DISTRO)-$(VERSION)

# Remove All Previous Updates Rolls
cleanupdates:
	- /sbin/service httpd stop
	- /opt/rocks/bin/rocks remove roll Updates-$(DISTRO)-$(VERSION) arch=$(ARCH)
	- /bin/rm Updates-$(DISTRO)-$(VERSION)-*.$(ARCH).*.iso
	- /sbin/service httpd start

testing:
	echo "arch is " $(ARCH)
