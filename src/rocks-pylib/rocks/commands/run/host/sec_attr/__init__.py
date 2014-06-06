import os
import sys

import pickle

import base64
import tempfile
import rocks.commands

import traceback
import cStringIO

class Command(rocks.commands.Command):
	"""
	This command reads a filename that contains
	pickled information about secure attributes
	that are relevant to the host.

	This command is not intended to be run by an
	administrator.
	<arg name="file" type="string">
	Filename of the pickled file
	</arg>
	"""
	def run(self, params, args):

		# The pickled file that was transported
		# out of band using scp
		fname = args[0]

		# Load the attribute dictionary, from the 
		# pickled file
		f = open(fname,'r')
		a_d = pickle.load(f)
		f.close()

		# For each attribute in the dict
		for a in a_d:
			# Get the value and filters
			value, filter = a_d[a][0], a_d[a][1]
			# If a filter exists - decode it, and use it
			if filter is not None:
				filter = base64.b64decode(filter)
				# Evaluate the filter
				try:
					# Import the filter
					exec filter
					p = plugin()
					# Run the filter against the value
					p.filter(value)
				except:
					# If there's an error in filtering,
					# it's very hard to get exception info out.
					# This alleviates that a bit.
					# Get the last traceback info and parse it
					tb = traceback.extract_tb(sys.exc_info()[2])[-1]
					# Get line information for the last traceback
					line_no = tb[1]
					# Print the error message
					print "Error in filter: line %d" % line_no
					print sys.exc_info()[0], ':', sys.exc_info()[1]
					# Print line from the filter that caused
					# the exception
					c = cStringIO.StringIO(filter).readlines()
					print c[line_no - 1]

		# Remove the pickled file
		os.unlink(fname)

RollName = "base"
