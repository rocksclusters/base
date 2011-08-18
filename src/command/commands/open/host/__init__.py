# $Id: __init__.py,v 1.3 2011/08/18 00:57:20 anoop Exp $

# @Copyright@
# @Copyright@

# $Log: __init__.py,v $
# Revision 1.3  2011/08/18 00:57:20  anoop
# Re-adding open host console command.
# This was accidentally removed in the cleanup of firewall commands
#

import rocks
import rocks.commands

class command(rocks.commands.open.command):
	pass
