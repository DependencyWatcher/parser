from dependencywatcher.parser.parser import Parser
from pyparsing import *

class SetupPyParser(Parser):

	def __init__(self, source):
		super(SetupPyParser, self).__init__(source)

		Comparison = Literal("<") | Literal("<=") | Literal("!=") | Literal("==") \
			 | Literal(">=") | Literal(">") | Literal("~=") | Literal("===")

		Version = Regex("[0-9][-A-Za-z0-9_.]+")
		VersionSpec = Group(Comparison + Version)
		VersionSpecList = Group(VersionSpec + ZeroOrMore(Suppress(Literal(",")) + VersionSpec))

		Identifier = Regex("[a-zA-Z][-A-Za-z0-9_.]+")
		ExtraList = Identifier + ZeroOrMore(Literal(",") + Identifier)
		Extras = Suppress(Literal("[") + ExtraList + Literal("]"))
		Requirement = Group(Identifier + Optional(VersionSpecList)) + Optional(Extras)
		QuotedRequirement = Suppress(Literal("\"")) + Requirement + Suppress(Literal("\"")) \
			| Suppress(Literal("'")) + Requirement + Suppress(Literal("'"))

		Args = QuotedRequirement + ZeroOrMore(Suppress(Literal(",")) + QuotedRequirement)
		ArgList = Suppress(Literal("[")) + Args + Suppress(Literal("]"))

		Kw = Suppress(Keyword("requires")) | Suppress(Keyword("install_requires")) \
			| Suppress(Keyword("setup_requires")) | Suppress(Keyword("extras_require"))
		self.parser = Kw + Suppress(Literal("=")) + ArgList
		self.parser.ignore(pythonStyleComment)

	def parse(self, dependencies):
		data = self.parser.searchString(self.source.get_content())
		if len(data) > 0:
			for d in data[0].asList():
				if len(d) == 2:
					dep_name = d[0]
					version = Parser.get_max_version(d[1])
					if version:
						dependencies.append({"name": dep_name, "version": version, "context": "python"})

Parser.register_parser(["setup\.py"], SetupPyParser)

