rpm:: build
	-cp *.x86_64.rpm $(REDHAT.RPMS)/$(ARCH)/
	-cp sun-javadb*.i386.rpm $(REDHAT.RPMS)/$(ARCH)/
