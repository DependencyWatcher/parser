from dependencywatcher.parser.parser import Parser
from dependencywatcher.parser.xml import XMLParser

class IvyParser(XMLParser):
	def load_vars(self, vars):
		for e in self.xml.xpath("//property"):
			try:
				vars[e.attrib["name"]] = e.attrib["value"]
			except KeyError:
				pass

	def parse(self, dependencies):
		for e in self.xml.xpath("/ivy-module/dependencies/dependency"):
			try:
				try:
					version = self.resolve(e.attrib["rev"])
				except KeyError:
					version = self.resolve(e.attrib["revision"])

				if not version.startswith("latest"):
					org = self.resolve(e.attrib["org"])
					name = self.resolve(e.attrib["name"])
					dependencies.append({
						"name": "%s:%s" % (org, name),
						"version": version,
						"context": "java",
						"line": e.sourceline
					})
			except KeyError:
				pass

Parser.register_parser([".*\.xml"], IvyParser)

