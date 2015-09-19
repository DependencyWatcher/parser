from dependencywatcher.parser.parser import Parser
from dependencywatcher.parser.pyparser import PyParser
from pyparsing import *

class SbtParser(PyParser):

    def __init__(self, source):
        super(SbtParser, self).__init__(source)

        vars = {}
        def store_var(st, locn, tokens):
            vars[tokens[0]] = tokens[1]
            return tokens

        def resolve_var(st, locn, tokens):
            try:
                tokens[0][2] = vars[tokens[0][2]]
            except KeyError:
                pass
            return tokens

        VersionSpec = Suppress(Literal("\"")) + Regex("[\[\]\(]?[0-9][-A-Za-z0-9_.\+\,]+[\[\]\)]?") + Suppress(Literal("\"")) 
        ScalaIdentifier = Regex("[a-zA-Z][A-Za-z0-9_.-]+")
        VarKeyword = Literal("val") | Literal("var")
        VarDeclaration = Suppress(VarKeyword) + ScalaIdentifier + Suppress(Literal("=")) + VersionSpec
        VarDeclaration.setParseAction(store_var)
        ArtifactIdentifier = Suppress(Literal("\"")) + Regex("[a-zA-Z][A-Za-z0-9_.-]+") + Suppress(Literal("\""))
        VarDependency = Group(ArtifactIdentifier + Suppress(Literal("%")) + ArtifactIdentifier + Suppress(Literal("%")) + ScalaIdentifier)
        VarDependency.setParseAction(resolve_var)
        Dependency = Group(ArtifactIdentifier + Suppress(Literal("%")) + ArtifactIdentifier + Suppress(Literal("%")) + VersionSpec)
        self.parser = VarDeclaration | VarDependency | Dependency
        self.parser.ignore(javaStyleComment)
        self.parser.setParseAction(self.defaultParseAction)

    def parse(self, dependencies):
        data = self.parser.searchString(self.source.get_content())
        for d in data.asList():
            for token in d:
                if len(token.data) == 3:
                    dep_name = "%s:%s" % (token.data[0], token.data[1])
                    version = token.data[2]
                    if version:
                        dependencies.append({"name": dep_name, "version": version, "context": "java", "line": token.line})

Parser.register_parser([".*\.sbt"], SbtParser)

