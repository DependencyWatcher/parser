from dependencywatcher.parser.parser import Parser
from dependencywatcher.parser.xml import XMLParser

class MavenParser(XMLParser):
	def load_vars(self, vars):
		for e in self.xml.xpath("//properties/*"):
			vars[e.tag] = e.text

	def parse(self, dependencies):
		for e in self.xml.xpath("//dependency|//parent"):
			try:
				version = self.resolve(e.find("version").text)
				if not version.endswith("-SNAPSHOT"):
					groupId = self.resolve(e.find("groupId").text)
					artifactId = self.resolve(e.find("artifactId").text)
					dependencies.append({
						"name": "%s:%s" % (groupId, artifactId),
						"version": version
					})
			except AttributeError:
				pass

Parser.register_parser(["pom\.xml"], MavenParser)

