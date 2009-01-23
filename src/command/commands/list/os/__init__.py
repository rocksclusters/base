# $Id: __init__.py,v 1.1 2009/01/23 23:46:51 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.1  2009/01/23 23:46:51  mjk
# - continue to kill off the var tag
# - can build xml and kickstart files for compute nodes (might even work)
#

import rocks.commands

class command(rocks.commands.list.command):
	pass
	
