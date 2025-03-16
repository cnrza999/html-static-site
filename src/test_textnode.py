import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://love/cherrybee")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://love/cherrybee")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a joker", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a joker", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_not_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://love/cherrybee")
        node2 = TextNode("This is a joker", TextType.BOLD, "https://loveko/bumblebee")
        self.assertNotEqual(node, node2)

    def test_repr_with_different_text_types(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(repr(node), "TextNode(This is a text node, italic, None)")

        node2 = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(repr(node2), "TextNode(This is a link, link, https://example.com)")

    def test_eq_with_none_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_text_type_enum(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_eq_with_empty_url(self):
        node = TextNode("This is a text node", TextType.LINK, "")
        node2 = TextNode("This is a text node", TextType.LINK, "")
        self.assertEqual(node, node2)

    def test_multiple_instances_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = node  # Same instance
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()