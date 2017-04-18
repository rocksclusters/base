ifeq ($(VERSION.MAJOR),5)
REPORPMS.NOARCH += elrepo-release-5-3.el5.elrepo.noarch.rpm
REPORPMS.NOARCH += epel-release-5-4.noarch.rpm
endif
ifeq ($(VERSION.MAJOR),6)
REPORPMS.NOARCH += elrepo-release-6-4.el6.elrepo.noarch.rpm
REPORPMS.NOARCH += epel-release-6-5.noarch.rpm
FAIL2BAN.PKGS = fail2ban python-inotify
endif
ifeq ($(VERSION.MAJOR),7)
# REPORPMS.NOARCH += elrepo-release-6-4.el6.elrepo.noarch.rpm
REPORPMS.NOARCH += epel-release-7-9.noarch.rpm
FAIL2BAN.PKGS = fail2ban fail2ban-firewalld fail2ban-sendmail fail2ban-server python-inotify
endif
