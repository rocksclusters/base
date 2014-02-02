rpm:: build
	for j in `ls *.x86_64.rpm.* | sed 's/rpm.*/rpm/' | sort | uniq`; do cat $$j.* > $$j; done 
	-cp *.x86_64.rpm $(REDHAT.RPMS)/$(ARCH)/
