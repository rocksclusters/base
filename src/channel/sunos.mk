install::
	mkdir -p $(ROOT)/$(PKGROOT)/share/channeld/
	$(INSTALL) -m0644 channeld.xml  $(ROOT)/$(PKGROOT)/share/channeld/channeld.xml
