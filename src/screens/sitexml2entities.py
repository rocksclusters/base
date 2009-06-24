#! /opt/rocks/bin/python
#
# @Copyright@
# @Copyright@
#
# $Log: sitexml2entities.py,v $
# Revision 1.1  2009/06/24 04:46:13  bruno
# restore roll tweaks
#

import rocks.util
import sys
import xml
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser
from xml.sax._exceptions import SAXParseException

class Handler(rocks.util.ParseXML):

	def startElement_var(self, name, attrs):
		name = attrs.get('name')
		val  = attrs.get('val')

		print '%s:%s' % (name, val)

parser  = make_parser()
parser.setContentHandler(Handler())
parser.parse(sys.stdin)





