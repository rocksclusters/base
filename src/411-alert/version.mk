NAME = rocks-411-alert
RELEASE = 1
RPM.ARCH = noarch
RPM.FILES = \
/opt/rocks/bin/*\\n\
/etc/serf/*

RPM.REQUIRES = rocks-411

RPM.DESCRIPTION = \
This is for handling 411 alerts via serf. This RPM should only be \\n\
installed on 411 client nodes, not a frontend. This utilizes Hashicorps \\n\
serf cluster membership for efficiency of operation.\\n

