from dependencywatcher.parser.parser import Parser
from StringIO import StringIO
from lxml import etree

class XMLParser(Parser):
	""" Abstract XML parser """
	def __init__(self, source):
		super(XMLParser, self).__init__(source)

		it = etree.iterparse(StringIO(source.get_content()))
		for _, el in it:
			try:
				el.tag = el.tag.split("}", 1)[1]  # strip all namespaces
			except IndexError:
				pass
		self.xml = it.root
		self.vars = {}
		self.load_vars(self.vars)

	def load_vars(self, vars):
		""" Load variables defined in the XML file """
		pass

	def resolve(self, text):
		""" Resolves all vars inside given text """
		for k, v in self.vars.iteritems():
			text = text.replace("${%s}" % k, v)
		return text

