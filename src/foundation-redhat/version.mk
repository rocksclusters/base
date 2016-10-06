NAME = foundation-redhat
RELEASE = 0

ifeq ($(strip $(VERSION.MAJOR)), 5)
RPMS = newt rpm-python rhpl
else
RPMS = newt rpm-python newt-python 
endif
RPM.FILES = "/opt/rocks/redhat/usr/bin/*\\n/opt/rocks/redhat/usr/lib64/lib*\\n/opt/rocks/redhat/usr/lib64/python2*/site-packages/*\\n/opt/rocks/redhat/usr/share/doc/*\\n/opt/rocks/redhat/usr/share/locale/*/LC_MESSAGES/*\\n/opt/rocks/redhat/usr/share/man/man[1-8]/*"
