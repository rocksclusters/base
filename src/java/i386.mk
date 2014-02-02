rpm:: build
	for j in `ls *.i[35]86.rpm.* | sed 's/rpm.*/rpm/' | sort | uniq`; do cat $$j.* > $$j; done 
	-cp *.i386.rpm $(REDHAT.RPMS)/$(ARCH)/
	-cp *.i586.rpm $(REDHAT.RPMS)/$(ARCH)/
