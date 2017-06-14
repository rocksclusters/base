NAME	=	rocks-sec-channel-server
RELEASE	=	2

SYSTEMDFOLDER = /etc/systemd/system
SYSTEMDINITSCRIPT = sec-channel.service
SYSVFOLDER = /etc/rc.d/init.d
SYSVINITSCRIPT = sec-channel 

ifeq ($(VERSION.MAJOR), 6)
SCRIPTSRC=sec-channel.init
SCRIPT=$(SYSVINITSCRIPT)
SCRIPTDEST=$(SYSVFOLDER)
endif
ifeq ($(VERSION.MAJOR), 7)
SCRIPTSRC=$(SYSTEMDINITSCRIPT)
SCRIPT=$(SYSTEMDINITSCRIPT)
SCRIPTDEST=$(SYSTEMDFOLDER)
endif

RPM.FILES = "$(SCRIPTDEST)/*\\n/opt/rocks/sbin/*"
