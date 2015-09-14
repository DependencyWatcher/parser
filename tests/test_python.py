from tests.parser import ParserTest

class PythonTest(ParserTest):
    def test_setup_py(self):
        self.assertParsable("python01", 3)
        
    def test_requirements_txt(self):
        self.assertParsable("python02", 4)
