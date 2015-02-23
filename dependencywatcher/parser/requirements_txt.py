from dependencywatcher.parser.parser import Parser, FileSource
import re, os

class RequirementsTxtParser(Parser):

	re_include = re.compile("-r\s+['\"]?([^\s'\"]+)")
	re_requirement = re.compile("(\w+)\s*([<=>].*)")
	re_restriction = re.compile("([<=>]+)\s*(\d\S+)")

	def __init__(self, source):
		super(RequirementsTxtParser, self).__init__(source)

	def _parse_restrictions(self, restrictions):
		version_specifiers = []
		for r in restrictions.split(","):
			m = self.re_restriction.match(r.strip())
			if m is not None:
				version_specifiers.append((m.group(1), m.group(2)))
		return Parser.get_max_version(version_specifiers)

	def _parse_requirements_txt_file(self, source, dependencies):
		for line_number, l in enumerate(source.get_content().splitlines()):
			m = self.re_include.search(l)
			if m is not None:
				include_file = m.group(1)
				if not os.path.isabs(include_file):
					include_file = os.path.join(os.path.dirname(source.filename), include_file)
				self._parse_requirements_txt_file(FileSource(include_file), dependencies)
			else:
				m = self.re_requirement.search(l)
				if m is not None:
					dep_name = m.group(1)
					version = self._parse_restrictions(m.group(2))
					if version is not None:
						dependencies.append({"name": dep_name, "version": version, "context": "python", "line": line_number + 1})

	def parse(self, dependencies):
		self._parse_requirements_txt_file(self.source, dependencies)

Parser.register_parser(["requirements\.txt"], RequirementsTxtParser)

