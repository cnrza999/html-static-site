import unittest

from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("def foo(): pass", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "def foo(): pass")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.png",
            "alt": "Alt text"
        })

    def test_link_missing_url(self):
        node = TextNode("Broken link!", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "TextNode of type LINK must have a URL")

    def test_image_missing_url(self):
        node = TextNode("Missing image source", TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "TextNode of type IMAGE must have a URL for 'src'")

    def test_invalid_type(self):
        class UnknownType:
            pass

        node = TextNode("Invalid type", UnknownType)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), f"Unsupported TextType: {node.text_type}")

    def test_not_a_textnode(self):
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node("Not a TextNode")
        self.assertEqual(str(context.exception), "Input must be an instance of TextNode")


if __name__ == "__main__":
    unittest.main()