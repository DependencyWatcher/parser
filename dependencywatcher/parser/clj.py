from dependencywatcher.parser.parser import Parser
from pyparsing import *

class CljProjectParser(Parser):

	def __init__(self, source):
		super(CljProjectParser, self).__init__(source)

		UnquotedArg = Word(alphanums + "-/.")
		QuotedArg = Suppress(Literal("\"")) + UnquotedArg + Suppress(Literal("\"")) \
			| Suppress(Literal("'")) + UnquotedArg + Suppress(Literal("'"))
		Arg = UnquotedArg | QuotedArg
		ArgList = Group(Suppress(Literal("[")) + Arg + Arg + Suppress(ZeroOrMore(Arg)) + Suppress(Literal("]")))
		List = Suppress(Literal("[")) + OneOrMore(ArgList) + Suppress(Literal("]"))
		self.parser = Suppress(Keyword(":dependencies")) + List

	def parse(self, dependencies):
		data = self.parser.searchString(self.source.get_content())
		for d in data[0].asList():
			dependencies.append({"name": d[0].replace("/", ":"), "version": d[1], "context": "java"})

Parser.register_parser(["project\.clj"], CljProjectParser)

