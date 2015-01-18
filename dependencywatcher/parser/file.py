from dependencywatcher.parser.parser import Parser
import re

class FileParser(Parser):
	patterns = [
		(re.compile("(.*?)[\-\_](\d.*)\.jar", re.I), "java"),
		(re.compile("(.*?)[\-\_](\d+\..*?)(\.min)?\.(js|css)", re.I), "js")
	]

	def parse(self, dependencies):
		for pattern, context in FileParser.patterns:
			m = pattern.match(self.source.get_name())
			if not m is None:
				dependencies.append({"name": m.group(1), "version": m.group(2), "context": context})

Parser.register_parser([".*\.(jar|js|css)"], FileParser)

