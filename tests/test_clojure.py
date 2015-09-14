from tests.parser import ParserTest

class ClojureTest(ParserTest):
    def test_lein_project(self):
        self.assertParsable("clojure01", 9)
        
