GRAPHVIZ_CPPFLAGS="-I/opt/sfw/include"
GRAPHVIZ_LDFLAGS="-L/opt/sfw/lib"

build:
	gunzip -c graphviz-$(VERSION).tar.gz | $(TAR) -xf -
	( 					\
		cd graphviz-$(VERSION);		\
		./configure --prefix=$(PKGROOT)	\
		--with-mylibgd			\
		LDFLAGS=$(GRAPHVIZ_LDFLAGS)	\
		CPPFLAGS=$(GRAPHVIZ_CPPFLAGS);	\
		$(MAKE);			\
	)
