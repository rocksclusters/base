NAME	= foundation-python-extras
RELEASE = 2
RPM.EXTRAS="%define _python_bytecompile_errors_terminate_build 0"
RPM.FILES="/opt/rocks/bin/*\\n/opt/rocks/include/gobject*\\n/opt/rocks/include/pycairo*\\n/opt/rocks/include/pygobject*\\n/opt/rocks/include/python2.7/*\\n/opt/rocks/lib/[a-oq-zA-Z]*\\n/opt/rocks/lib/pkgconfig/*\\n/opt/rocks/lib/pyg*\\n/opt/rocks/lib/python2.7/site-packages/*\\n/opt/rocks/share/aclocal/*\\n/opt/rocks/share/[a-ln-zA-Z]*\\n/opt/rocks/share/man/man1/*"
