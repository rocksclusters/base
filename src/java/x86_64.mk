rpm:: build
	-cp *.x86_64.rpm $(REDHAT.RPMS)/$(ARCH)/
	-cp *.i586.rpm $(REDHAT.RPMS)/$(ARCH)/
	-cp *.i386.rpm $(REDHAT.RPMS)/$(ARCH)/
