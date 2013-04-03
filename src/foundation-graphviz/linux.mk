build:
	gunzip -c graphviz-$(VERSION).tar.gz | $(TAR) -xf -
	( 					\
		cd graphviz-$(VERSION);		\
		./configure --prefix=$(PKGROOT) \
		--enable-perl=no --enable-python=no;\
		$(MAKE);			\
	)
