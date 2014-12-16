from dependencywatcher.parser.parser import Parser
import re

class GemfileParser(Parser):
	gem_re = re.compile("^\s*gem\s+(.*)", re.I | re.M)
	version_re = [re.compile("^(\d\S+)"), re.compile("\<=?\s*(\d\S+)")]

	def parse(self, dependencies):
		for gem in GemfileParser.gem_re.finditer(self.source.get_content()):
			params = [p.strip("'\"\t ") for p in gem.group(1).split(",")]
			for param in params[1:]:
				for r in GemfileParser.version_re:
					m = r.search(param)
					if m:
						dependencies.append({
							"name": params[0],
							"version": m.group(1),
							"context": "ruby"
						});
						break

Parser.register_parser(["Gemfile"], GemfileParser)

