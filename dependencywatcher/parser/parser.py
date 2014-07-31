import re, os

class FileSource(object):
	def __init__(self, filename, content=None):
		self.filename = filename
		self.content = content

	def get_name(self):
		""" Returns base name of the source file """
		try:
			return self.basename
		except AttributeError:
			self.basename = os.path.basename(self.filename)
		return self.basename

	def get_content(self):
		if self.content is None:
			with open(self.filename) as f:
				self.content = f.read()
		return self.content


class Parser(object):
	parsers = {}

	def __init__(self, source):
		self.source = source

	def parse(self, dependencies):
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
		source = FileSource(filename)
		for pattern, parsers in Parser.parsers.iteritems():
			if re.match(pattern, source.get_name(), re.I):
				for parser in parsers:
					yield parser(source)

	@staticmethod
	def filter_dependencies(dependencies):
		u = {}
		for dep in dependencies:
			u["%s-%s" % (dep["name"], dep["version"])] = dep
		return u.values()

	@staticmethod
	def parse_dir(dir): 
		dependencies = []
		for root, dirs, files in os.walk(dir):
			for name in files:
				for p in Parser.get_parsers(os.path.join(root, name)):
					p.parse(dependencies)
		return Parser.filter_dependencies(dependencies)

