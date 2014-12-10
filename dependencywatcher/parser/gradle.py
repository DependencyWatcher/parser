from dependencywatcher.parser.parser import Parser
import re

class GradleParser(Parser):
	deps_list_re = re.compile("dependencies\s+\{([^\}]+)\}", re.M|re.I)
	dep_line_re = [
		re.compile("(?:classpath|compile)\s+[\'\"]?(.*):(\d[^\'\"]*)", re.I)
	]

	def parse(self, dependencies):
		for deps_list in GradleParser.deps_list_re.finditer(self.source.get_content()):
			for r in GradleParser.dep_line_re:
				for e in r.finditer(deps_list.group(1)):
					dependencies.append({
						"name": e.group(1),
						"version": e.group(2),
						"context": "java"
					})

Parser.register_parser(["build\.gradle"], GradleParser)

