from tests.parser import ParserTest

class MavenTest(ParserTest):
    def test_maven_project(self):
        self.assertParsable("maven01", 9)
        
