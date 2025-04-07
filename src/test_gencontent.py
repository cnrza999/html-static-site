import unittest

from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        actual = extract_title("# Hello")
        self.assertEqual(actual, "Hello")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title
    
# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list  
"""
        )
        self.assertEqual(actual, "title")

    def test_no_title(self):
        try:
            extract_title(
                """
no title here
                """
            )
            self.fail("Expected an exception")
        except Exception as e:
            pass

if __name__ == "__main__":
    unittest.main()