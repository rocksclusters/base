build:
	gunzip -c wget-$(VERSION).tar.gz | $(TAR) -xf -
	( 					\
		cd wget-$(VERSION);		\
		./configure --prefix=$(PKGROOT);\
		$(MAKE);			\
	)
