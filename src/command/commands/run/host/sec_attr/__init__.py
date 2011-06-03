import os
import sys

import pickle

import base64
import tempfile
import rocks.commands

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
				exec filter
				p = plugin()
				# Run the filter against the value
				p.filter(value)

		# Remove the pickled file
		os.unlink(fname)
