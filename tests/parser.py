import unittest, os, re
from dependencywatcher.parser.parser import Parser

class ParserTest(unittest.TestCase):
    """ Abstract parser unit test """

    def assertHasInfo(self, parsed_info, keys):
        for k in keys:
            self.assertIsNotNone(parsed_info[k])

    def assertHasAllInfo(self, parsed_info):
        self.assertHasInfo(parsed_info, ["file", "line", "version", "name", "context"])
        self.assertTrue(re.match(r"[0-9][-A-Za-z0-9_.]+", parsed_info["version"]), "Parsed version is not correct: %s" % parsed_info["version"])

    def assertParsable(self, project_dir, num_dependencies):
        parsed_info = Parser.parse_dir(os.path.join(os.path.dirname(__file__), "projects", project_dir))
        self.assertEquals(num_dependencies, len(parsed_info),
                "%s: number of dependencies doesn't match (expected: %d, actual: %d)" % (project_dir, num_dependencies, len(parsed_info)))
        for i in parsed_info:
            self.assertHasAllInfo(i)

