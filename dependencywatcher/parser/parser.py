import re, os, logging
from multiprocessing.pool import ThreadPool

logger = logging.getLogger(__name__)

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
	concurrency = 2

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
		for pattern, parser_classes in Parser.parsers.iteritems():
			if re.match(pattern, source.get_name(), re.I):
				for parser_class in parser_classes:
					try:
						yield parser_class(source)
					except Exception as e:
						#logger.exception(e)
						logger.warning("[%s] can't parse file: %s" % (parser_class.__name__, filename))

	@staticmethod
	def filter_dependencies(dependencies):
		u = {}
		for dep in dependencies:
			u["%s-%s-%s" % (dep["name"], dep["version"], dep["context"])] = dep
		return u.values()


	@staticmethod
	def parse_file(file):
		dependencies = []
		for p in Parser.get_parsers(file):
			try:
				p.parse(dependencies)
			except Exception as e:
				#logger.exception(e)
				logger.warning("[%s] can't parse file: %s" % (p.__class__.__name__, file))
		return dependencies

	@staticmethod
	def parse_dir(dir): 
		pool = ThreadPool(processes=Parser.concurrency)
		dependencies = []
		def callback(res):
			dependencies.extend(res)
		for root, dirs, files in os.walk(dir):
			for name in files:
				pool.apply_async(Parser.parse_file, args = (os.path.join(root, name),), callback = callback)
		pool.close()
		pool.join()
		return Parser.filter_dependencies(dependencies)

