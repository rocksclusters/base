build:
	gunzip -c graphviz-$(VERSION).tar.gz | $(TAR) -xf -
	( 					\
		cd graphviz-$(VERSION);		\
		./configure --prefix=$(PKGROOT);\
		$(MAKE);			\
	)
