from dependencywatcher.parser.parser import Parser
from pyparsing import lineno

class PyParser(Parser):
	""" Abstract parser that uses pyparsing module """

	class Token(object):
		def __init__(self, st, locn, data):
			self.data = data
			self.line = lineno(locn,st)

		@classmethod
		def create(cls, st, locn, data):
			return [cls(st, locn, d) for d in data]

	def __init__(self, source):
		super(PyParser, self).__init__(source)
		self.defaultParseAction = PyParser.Token.create

