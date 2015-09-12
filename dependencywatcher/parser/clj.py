from dependencywatcher.parser.parser import Parser
from dependencywatcher.parser.pyparser import PyParser
from pyparsing import *

class CljProjectParser(PyParser):

    def __init__(self, source):
        super(CljProjectParser, self).__init__(source)

        Comment = Regex(r";.*")
        UnquotedArg = Word(alphanums + "-/.")
        QuotedArg = Suppress(Literal("\"")) + UnquotedArg + Suppress(Literal("\"")) \
            | Suppress(Literal("'")) + UnquotedArg + Suppress(Literal("'"))
        CljKeyword = Suppress(Literal(":")) + Word(alphanums + "-._")
        List = Forward()
        ArgList = Forward()
        Arg = UnquotedArg | QuotedArg | CljKeyword | ArgList | List
        ArgList << Group(Suppress(Literal("[")) + Arg + ZeroOrMore(Arg) + Suppress(Literal("]")))
        ArgList.ignore(Comment)
        List << Suppress(Literal("[")) + OneOrMore(ArgList) + Suppress(Literal("]"))
        self.parser = (Suppress(Keyword(":dependencies")) + List)
        self.parser.setParseAction(self.defaultParseAction)

    def parse(self, dependencies):
        data = self.parser.searchString(self.source.get_content())
        for d in data:
            for token in d.asList():
                dependencies.append({"name": token.data[0].replace("/", ":"), "version": token.data[1], "context": "java", "line": token.line})

Parser.register_parser(["project\.clj"], CljProjectParser)

