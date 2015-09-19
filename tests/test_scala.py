from tests.parser import ParserTest

class ScalaTest(ParserTest):
    def test_sbt(self):
        self.assertParsable("scala01", 12)
        
