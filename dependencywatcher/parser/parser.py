import re, os

class Parser(object):
	parsers = {}

	def __init__(self, contents):
		self.contents = contents

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
	def get_parsers(filename, contents=None):
		""" Returns all compatible parsers for the given filename """
		basename = os.path.basename(filename)
		for pattern, parsers in Parser.parsers.iteritems():
			if re.match(pattern, basename, re.IGNORECASE):
				for parser in parsers:
					if contents is None:
						with open(filename) as f:
							contents = f.read()
					yield parser(contents)

