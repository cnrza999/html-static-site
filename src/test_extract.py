import unittest
from extract_tag import extract_title
from splitnode import extract_markdown_images, extract_markdown_links

class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        matches = extract_markdown_images(text)

        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        matches = extract_markdown_links(text)

        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_single_h1_header(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_extra_spaces(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_multiple_lines_with_h1(self):
        markdown = "Random text\n# Header 1\n## Header 2"
        self.assertEqual(extract_title(markdown), "Header 1")

    def test_no_h1_header(self):
        with self.assertRaises(ValueError):
            extract_title("Random text\n## Header 2")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_h1_not_at_start_of_line(self):
        with self.assertRaises(ValueError):
            extract_title("Text before # H1 Header")

    def test_multiple_h1_headers(self):
        markdown = "# First H1\n# Second H1"
        self.assertEqual(extract_title(markdown), "First H1")

    def test_only_h1_header(self):
        self.assertEqual(extract_title("# H1 Only"), "H1 Only")

    def test_h1_header_with_special_characters(self):
        self.assertEqual(extract_title("# @Header-123!"), "@Header-123!")

    def test_h1_header_with_markdown_formatting(self):
        self.assertEqual(extract_title("# **Bold Header**"), "**Bold Header**")

    if __name__ == "__main__":
        unittest.main()