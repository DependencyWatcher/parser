from dependencywatcher.parser.parser import Parser
import re, os

class JarFileParser(Parser):
	jarfile_re = re.compile("(.*?)[\-\_](\d.*)\.jar", re.I)

	def parse(self):
		dependencies = []
		m = JarFileParser.jarfile_re.match(self.source.get_name())
		if not m is None:
			dependencies.append({"name": m.group(1), "version": m.group(2)})
		return dependencies

Parser.register_parser([".*\.jar"], JarFileParser)

