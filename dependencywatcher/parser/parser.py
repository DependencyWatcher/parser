import re, os

class Parser(object):
	parsers = {}

	def __init__(self, filename):
		self.filename = filename
		self.contents = None

	def get_contents(self):
		if self.contents is None:
			with open(self.filename) as f:
				self.contents = f.read()
		return self.contents

	def parse(self):
		""" Returns list of dependencies required by this file """
		raise NotImplementedError

	@staticmethod
	def register_parser(patterns, parser):
		""" Registers new parser for the given set of file patterns """
		for p in patterns:
			try:
				Parser.parsers[p].append(parser)
			except KeyError:
				Parser.parsers[p] = [parser]

	@staticmethod
	def get_parsers(filename):
		""" Returns all compatible parsers for the given filename """
		basename = os.path.basename(filename)
		for pattern, parsers in Parser.parsers.iteritems():
			if re.match(pattern, basename, re.I):
				for parser in parsers:
					yield parser(filename)

