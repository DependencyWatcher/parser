from dependencywatcher.parser.parser import Parser
from lxml import html
from urlparse import urlparse
import re

class HTMLParser(Parser):
	patterns = [
		(re.compile("/ajax.googleapis.com/ajax/libs/([^/]+)/([^/]+)"), ([1, 2])),
		(re.compile("/cdn.jsdelivr.net/([^/]+)/(\d[^/]+)"), ([1, 2])),
		(re.compile("/netdna.bootstrapcdn.com/([^/]+)/([^/]+)"), ([1, 2])),
		(re.compile("/cdnjs.cloudflare.com/ajax/libs/([^/]+)/([^/]+)"), ([1, 2])),
		(re.compile("/([^/]+)-(\d[^/]+)\.min\.js"), ([1, 2])),
		(re.compile("/([^/]+)-(\d[^/]+)\.js"), ([1, 2]))
	]
	inline_patterns = [
		(re.compile("/cdn.jsdelivr.net/g/(.*)"), re.compile("([^/,@()]+)@(\d[^/,()]+)"))
	]

	def __init__(self, source):
		super(HTMLParser, self).__init__(source)
		self.root = html.document_fromstring(source.get_content())

	def create_dependency(self, name, version):
		return {"name": name, "version": version, "context": "js"}

	def parse_href(self, href):
		for pattern, order in HTMLParser.patterns:
			m = pattern.search(href)
			if m:
				return [self.create_dependency(m.group(order[0]), m.group(order[1]))]

		for href_pattern, dep_pattern in HTMLParser.inline_patterns:
			m = href_pattern.search(href)
			if m:
				inline_deps = []
				for m2 in dep_pattern.finditer(m.group(1)):
					inline_deps.append(self.create_dependency(m2.group(1), m2.group(2)))
				if len(inline_deps) > 0:
					return inline_deps
		return []

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
			dependencies.extend(self.parse_href(href))

	def parse(self, dependencies):
		self.find_deps("script", ["src", "data-src"], dependencies)
		self.find_deps("link", ["href"], dependencies)

Parser.register_parser([".*\.html?", ".*\.ftl", ".*\.php[345s]?", ".*\.phtml", ".*\.jsp"], HTMLParser)

