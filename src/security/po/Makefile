

MSGFMT=/usr/bin/msgfmt

LOCALDIR=/usr/share/locale


build:: 
	for f in `find ./ -name "*.po"`; do \
		$(MSGFMT)  -o `basename $$f .po`.mo $$f ;\
	done

install:
	for f in `ls -1 *.mo`;do \
		install -m0644  $$f /usr/share/locale/`basename $$f .mo`/LC_MESSAGES/insert-access.mo ;\
	done

clean ::
	rm -f *.mo

