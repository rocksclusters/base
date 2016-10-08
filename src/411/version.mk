NAME = rocks-411
RELEASE = 1
RPM.ARCH = noarch
RPM.FILES = \
/opt/rocks/bin/*\\n\
/opt/rocks/etc/*\\n\
/opt/rocks/lib/python2*/site-packages/rocks/*

RPM.DESCRIPTION = \
The 411 Secure Information Service. This facility is intended to replace \\n\
NIS which has security and scaling issues. 411 uses public-key \\n\
cryptography to securely distribute sensitive files such as group and \\n\
shadow password files. 411 uses either HTTP or HTTPS as its transport \\n\
protocol, however 411 is designed to maintain full security even with \\n\
regular HTTP. The 411 service leverages Ganglia to work at its highest \\n\
efficiency, although Ganglia is not a prerequisite for correct \\n\
operation.

