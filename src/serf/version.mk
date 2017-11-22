PKGROOT	= /opt/rocks/bin
NAME	= serf
RELEASE = 0
VERSION = 0.8.1
ZIPFILE = $(NAME)_$(VERSION)_linux_amd64.zip

INITD_DIR	= /etc/init.d
INITD_SCRIPTS	= rocks-serf
SYSTEMD_DIR	= /etc/systemd/system
SYSTEMD_SCRIPTS = rocks-serf.service

ifeq ($(VERSION.MAJOR),6)
SCRIPTMODE = 755
SCRIPTDIR = $(INITD_DIR)
SCRIPTS = $(INITD_SCRIPTS)
endif
ifeq ($(VERSION.MAJOR),7)
SCRIPTMODE = 644
SCRIPTDIR = $(SYSTEMD_DIR)
SCRIPTS = $(SYSTEMD_SCRIPTS)
RSYSLOGDIR = /etc/rsyslog.d
RSYSLOG_SCRIPT = serf.conf 
endif

RPM.FILES	= \
$(PKGROOT)/*\n\
/var/opt/rocks/$(NAME)\n\
/etc/$(NAME)\n\
/etc/logrotate.d/*\n\
$(SCRIPTDIR)/*\n\

ifeq ($(VERSION.MAJOR),7)
RPM.FILES += $(RSYSLOGDIR)/*
endif
