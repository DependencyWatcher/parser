from dependencywatcher.parser.parser import Parser
from dependencywatcher.parser.file import FileParser
import os

class FileListParser(FileParser):
	def __init__(self, source):
		super(FileListParser, self).__init__(source)
		self.filenames = source.get_content().splitlines()

	def parse(self, dependencies):
		for fn in self.filenames:
			basefn = os.path.basename(fn)
			for pattern, context in FileParser.patterns:
				m = pattern.match(basefn)
				if not m is None:
					dependencies.append({"file": fn, "name": m.group(1), "version": m.group(2), "context": context})

Parser.register_parser(["DWFileList.txt"], FileListParser)

