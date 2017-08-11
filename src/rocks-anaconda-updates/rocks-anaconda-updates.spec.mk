# This file is called from the generated spec file.
# It can also be used to debug rpm building.
# 	make -f rocks-anaconda-updates.spec.mk build|install

ifndef __RULES_MK
build:
	make ROOT=/export/home/repositories/rocks/src/roll/base/src/rocks-anaconda-updates/rocks-anaconda-updates.buildroot build

install:
	make ROOT=/export/home/repositories/rocks/src/roll/base/src/rocks-anaconda-updates/rocks-anaconda-updates.buildroot install
endif
