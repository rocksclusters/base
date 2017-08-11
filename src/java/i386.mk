rpm:: build
	( for j in *i586.rpm; do  \
		destname=`/usr/bin/rpm -qip $$j | awk -f rpmname.awk`; \
		/bin/cp $$j $(REDHAT.RPMS)/$(ARCH)/$$destname;\
	  done; \
	)
