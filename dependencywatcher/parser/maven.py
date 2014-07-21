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
		self.init_props()

	def init_props(self):
		self.props = {}
		for e in self.xml.xpath("//properties/*"):
			self.props[e.tag] = e.text

	def resolve(self, text):
		""" Resolves all properties inside given text """
		for k, v in self.props.iteritems():
			text = text.replace("${%s}" % k, v)
		return text

	def parse(self):
		dependencies = []
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
		return dependencies

Parser.register_parser(["pom\.xml"], MavenParser)

