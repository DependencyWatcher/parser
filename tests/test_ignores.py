from tests.parser import ParserTest

class IgnoresTest(ParserTest):
    def test_ignores(self):
        self.assertParsable("ignore01", 1)
        
