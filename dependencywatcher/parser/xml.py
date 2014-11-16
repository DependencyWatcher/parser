from dependencywatcher.parser.parser import Parser
from StringIO import StringIO
from lxml import etree
import re

class XMLParser(Parser):
	RE_VAR = re.compile("\$\{([^\}]+)\}")

	""" Abstract XML parser """
	def __init__(self, source):
		super(XMLParser, self).__init__(source)

		it = etree.iterparse(StringIO(source.get_content()), resolve_entities=False)
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
		prev_text = text
		while True:
			for k, v in self.vars.iteritems():
				if v is None:
					v = ""
				text = text.replace("${%s}" % k, v)
			if not XMLParser.RE_VAR.match(text) or text == prev_text:
				break
		return text

