# $Id: __init__.py,v 1.1 2009/02/10 20:11:20 mjk Exp $
#
# @Copyright@
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.1  2009/02/10 20:11:20  mjk
# os attr stuff for anoop
#

import rocks.commands

class command(rocks.commands.OSArgumentProcessor,
	rocks.commands.remove.command):
	pass
	
