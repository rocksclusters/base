NAME = foundation-redhat
RELEASE = 0

ifeq ($strip $(VERSION.MAJOR), 5)
RPMS = newt rpm-python rhpl
else
RPMS = newt rpm-python newt-python 
endif
