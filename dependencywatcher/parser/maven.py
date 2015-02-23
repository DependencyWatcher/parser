from dependencywatcher.parser.parser import Parser
from dependencywatcher.parser.xml import XMLParser
import traceback

class MavenParser(XMLParser):
	def load_vars(self, vars):
		for e in self.xml.xpath("//properties/*"):
			vars[e.tag] = e.text
		proj_version = self.xml.xpath("/project/version/text()")
		if len(proj_version) == 0:
			proj_version = self.xml.xpath("/project/parent/version/text()")
		if len(proj_version) > 0:
			vars["pom.version"] = vars["project.version"] = proj_version[0].strip()

	def parse(self, dependencies):
		for e in self.xml.xpath("//dependency|//parent"):
			try:
				version_elem = e.find("version")
				version = self.resolve(version_elem.text)
				if not version.endswith("-SNAPSHOT") and not XMLParser.RE_VAR.match(version):
					groupId = self.resolve(e.find("groupId").text)
					artifactId = self.resolve(e.find("artifactId").text)
					dependencies.append({
						"name": "%s:%s" % (groupId, artifactId),
						"version": version,
						"context": "java",
						"line": version_elem.sourceline
					})
			except AttributeError:
				pass

Parser.register_parser(["pom\.xml"], MavenParser)

