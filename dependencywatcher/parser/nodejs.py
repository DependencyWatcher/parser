from dependencywatcher.parser.parser import Parser
from dependencywatcher.parser.json import JSONParser
import re

class NodeJSParser(JSONParser):
	version_re = [re.compile("^(\d\S+)"), re.compile("\<(\d\S+)")]

	def parse(self, dependencies):
		for f in ["dependencies", "devDependencies"]:
			if f in self.json:
				for name, range in self.json[f].iteritems():
					for r in NodeJSParser.version_re:
						m = r.search(range)
						if m:
							dependencies.append({
								"name": name,
								"version": m.group(1),
								"context": "nodejs"
							});

Parser.register_parser(["package\.json"], NodeJSParser)

