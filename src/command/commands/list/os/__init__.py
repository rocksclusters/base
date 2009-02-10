# $Id: __init__.py,v 1.2 2009/02/10 20:11:20 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.2  2009/02/10 20:11:20  mjk
# os attr stuff for anoop
#
# Revision 1.1  2009/01/23 23:46:51  mjk
# - continue to kill off the var tag
# - can build xml and kickstart files for compute nodes (might even work)
#

import rocks.commands

class command(rocks.commands.OSArgumentProcessor, rocks.commands.list.command):
	pass
	
