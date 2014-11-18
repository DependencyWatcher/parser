from dependencywatcher.parser.parser import Parser
from lxml import html
from urlparse import urlparse
import re

class HTMLParser(Parser):
	patterns = [
		(re.compile("/ajax.googleapis.com/ajax/libs/([^/]+)/([^/]+)"), ([1, 2])),
		(re.compile("/cdn.jsdelivr.net/([^/]+)/([^/]+)"), ([1, 2])),
		(re.compile("/netdna.bootstrapcdn.com/([^/]+)/([^/]+)"), ([1, 2])),
		(re.compile("/cdnjs.cloudflare.com/ajax/libs/([^/]+)/([^/]+)"), ([1, 2])),
		(re.compile("/([^/]+)-(\d[^/]+)\.min\.js"), ([1, 2])),
		(re.compile("/([^/]+)-(\d[^/]+)\.js"), ([1, 2]))
	]

	def __init__(self, source):
		super(HTMLParser, self).__init__(source)
		self.root = html.document_fromstring(source.get_content())

	def parse_href(self, href):
		for pattern, order in HTMLParser.patterns:
			m = pattern.search(href)
			if m:
				return {"name": m.group(order[0]), "version": m.group(order[1])}
		return None

	def get_hrefs(self, tag, attrs):
		for e in self.root.xpath("//%s" % tag):
			for attr in attrs:
				try:
					yield e.attrib[attr]
					break
				except KeyError:
					continue

	def find_deps(self, tag, attrs, dependencies):
		for href in self.get_hrefs(tag, attrs):
			dependency = self.parse_href(href)
			if dependency:
				dependencies.append(dependency)

	def parse(self, dependencies):
		self.find_deps("script", ["src", "data-src"], dependencies)
		self.find_deps("link", ["href"], dependencies)

Parser.register_parser([".*\.html?", ".*\.ftl", ".*\.php[345s]?", ".*\.phtml", ".*\.jsp"], HTMLParser)

