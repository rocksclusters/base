ifeq ($(VERSION.MAJOR),5)
REPORPMS.NOARCH += elrepo-release-5-3.el5.elrepo.noarch.rpm
REPORPMS.NOARCH += epel-release-5-4.noarch.rpm
else
REPORPMS.NOARCH += elrepo-release-6-4.el6.elrepo.noarch.rpm
REPORPMS.NOARCH += epel-release-6-5.noarch.rpm
endif
