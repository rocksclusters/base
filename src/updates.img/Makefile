REDHAT.ROOT     = $(CURDIR)/../../
ROCKSROOT       = ../../../../..

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

IMAGESDIR	= ../web-server/src/www.rockclusters.org/images
IMAGES		= nsfwantsyou.png \
		  pyramids.png rocks-avalanche-logo.png


install-images:
	for i in $(IMAGES) ; do \
		cp $(REDHAT.ROOT)/$(IMAGESDIR)/$$i pixmaps/rnotes/ ; \
	done

build:	install-images
	./build-updates-img.py
	dd if=/dev/zero of=updates.img bs=1024 \
		count=`du -s -k extra | awk '{ print int($$1*1.1) }'`
	echo y | /sbin/mkfs -t ext2 updates.img
	mkdir mnt
	mount -o loop updates.img mnt
	mkdir -p mnt/pixmaps
	cp pixmaps/*png mnt/pixmaps
	mkdir -p mnt/pixmaps/rnotes
	cp pixmaps/rnotes/*png mnt/pixmaps/rnotes
	(cd extra && cp --recursive . ../mnt)
	umount mnt

install::
	mkdir -p $(ROOT)/images
	install -ma+r updates.img $(ROOT)/images
	mkdir -p $(ROOT)/RedHat/base
	install -ma+r comps.xml $(ROOT)/RedHat/base

clean::
	rm -f updates.img
	rm -f $(SPECFILE).in
	rm -rf mnt
	rm -rf extra
	rm -rf rocks-dist
	( cd pixmaps/rnotes ; rm -f $(IMAGES) )
