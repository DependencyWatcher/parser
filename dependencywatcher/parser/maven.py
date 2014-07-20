from dependencywatcher.parser.parser import Parser
from StringIO import StringIO
from lxml import etree

class MavenParser(Parser):
	def __init__(self, contents):
		super(MavenParser, self).__init__(contents)
		it = etree.iterparse(StringIO(contents))
		for _, el in it:
			el.tag = el.tag.split("}", 1)[1]  # strip all namespaces
		self.xml = it.root

		self.props = {}
		for e in self.xml.xpath("//properties/*"):
			self.props[e.tag] = e.text

	def parse(self):
		dependencies = []
		for e in self.xml.xpath("//dependency"):
			try:
				dependencies.append({
					"name": "%s:%s" % (e.find("groupId").text, e.find("artifactId").text),
					"version": e.find("version").text
				})
			except KeyError:
				pass
		return dependencies

Parser.register_parser(["pom\.xml"], MavenParser)

