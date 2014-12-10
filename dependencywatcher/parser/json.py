from __future__ import absolute_import
from dependencywatcher.parser.parser import Parser
from StringIO import StringIO
import json as j

class JSONParser(Parser):
	""" Abstract JSON parser """
	def __init__(self, source):
		super(JSONParser, self).__init__(source)
		self.json = j.load(StringIO(source.get_content()))

