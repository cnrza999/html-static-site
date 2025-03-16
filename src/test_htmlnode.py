import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_no_prop(self):
        node1 = HTMLNode(tag="p", value="bakana")
        self.assertEqual(node1.props_to_html(), "")

    def test_single_attr(self):
        node2 = HTMLNode(tag="a", value="Click here", props={"href": "https://google.com"})
        self.assertEqual(node2.props_to_html(), ' href="https://google.com"')

    def test_multiple_attr(self):
        node3 = HTMLNode(
            tag="img",
            props={"src": "image.png", "alt": "An image", "width": "100"}
        )
        expected_output = ' src="image.png" alt="An image" width="100"'
        self.assertEqual(node3.props_to_html(), expected_output)

    def test_none_tag(self):
        node = HTMLNode(tag=None, value="This is raw text")
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props(self):
        node = HTMLNode(tag="p", value="No attributes", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_none_props(self):
        node = HTMLNode(tag="input", value="Test input", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_special_chars_in_props(self):
        node = HTMLNode(
            tag="a",
            value="Link with special chars",
            props={"href": "https://example.com?foo=bar&baz=qux"}
        )
        expected_output = ' href="https://example.com?foo=bar&baz=qux"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_multiple_children(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(len(parent.children), 2)

    def test_none_value(self):
        node = HTMLNode(tag="a", value=None, props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_multiple_spaces_in_props(self):
        node = HTMLNode(tag="input", props={" type": " text ", " value ": "hello"})
        expected_output = ' type="text" value="hello"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_boolean_attributes(self):
        node = HTMLNode(tag="input", props={"type": "checkbox", "checked": True})
        expected_output = ' type="checkbox" checked'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_no_value(self):
        node = HTMLNode(tag="input", value=None, props={"type": "text"})
        expected_output = ' type="text"'
        self.assertEqual(node.props_to_html(), expected_output)

if __name__ == "__main__":
    unittest.main()

