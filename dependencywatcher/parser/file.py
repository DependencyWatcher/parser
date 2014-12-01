from dependencywatcher.parser.parser import Parser
import re, os

class FileParser(Parser):
	patterns = [
		re.compile("(.*?)[\-\_](\d.*)\.jar", re.I),
		re.compile("(.*?)[\-\_](\d.*?)(\.min)?\.(js|css)", re.I)
	]

	def parse(self, dependencies):
		for p in FileParser.patterns:
			m = p.match(self.source.get_name())
			if not m is None:
				dependencies.append({"name": m.group(1), "version": m.group(2)})

Parser.register_parser([".*\.(jar|js|css)"], FileParser)

