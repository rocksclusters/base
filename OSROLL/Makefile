## Makefile to create an OS Roll and Updates
## $Id: Makefile,v 1.3 2012/02/24 02:01:53 clem Exp $
## $Log: Makefile,v $
## Revision 1.3  2012/02/24 02:01:53  clem
## os roll and update roll was always built for 6.2 (now it build also for 5.7)
##
## Revision 1.2  2011/11/11 06:00:24  phil
## Updated anaconda to RHEL 5.7 base
##
## Revision 1.1  2011/11/02 16:43:38  phil
## In bootstrap0, create an OS and Updates roll after the Rocks database is up and running.
##
SHELL = /bin/bash
#needs this to include proper version number
ROLLSROOT = $(CURDIR)/../src/devel/devel/src/roll
-include $(ROLLSROOT)/etc/Rolls.mk



include version.mk
WORKDIR = /tmp/OSROLL
default: updates 

# Create the Base OS Roll
base: workdir
	( cd $(WORKDIR);\
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(BASEPATH) arch=$(ARCH) rollname=$(DISTRO) version=$(VERSION) )
	- /sbin/service httpd stop 
	/opt/rocks/bin/rocks add roll $(WORKDIR)/$(DISTRO)-$(VERSION)-*.iso
	- /sbin/service httpd start
	/opt/rocks/bin/rocks enable roll $(DISTRO)

# Mirror Updates, then add to distro
updates: workdir cleanupdates
	(cd $(WORKDIR) ;\
	/opt/rocks/bin/rocks create mirror $(MIRRORURL)/$(UPDATESPATH) arch=$(ARCH) rollname=Updates-$(DISTRO)-$(VERSION) version="`date +%F`" )
	- /sbin/service httpd stop
	/opt/rocks/bin/rocks add roll $(WORKDIR)/Updates-$(DISTRO)-$(VERSION)-*.$(ARCH).*.iso
	-/sbin/service httpd start
	/opt/rocks/bin/rocks enable roll Updates-$(DISTRO)-$(VERSION)

# Remove All Previous Updates Rolls
cleanupdates: workdir
	- /sbin/service httpd stop
	- /opt/rocks/bin/rocks remove roll Updates-$(DISTRO)-$(VERSION) arch=$(ARCH)
	- /bin/rm $(WORKDIR)/Updates-$(DISTRO)-$(VERSION)-*.$(ARCH).*.iso
	- /sbin/service httpd start

workdir:
	if [ ! -d $(WORKDIR) ]; then mkdir -p $(WORKDIR); fi

clean:: workdir
	/bin/rm $(WORKDIR)/*iso

testing:
	echo "arch is " $(ARCH)
