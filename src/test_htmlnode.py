import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_strong(self):
        node = LeafNode("strong", "Joker!")
        self.assertEqual(node.to_html(), "<strong>Joker!</strong>")

    def test_leaf_to_html_no_tag_raw_text(self):
        node = LeafNode(None, "This is plain text.")
        self.assertEqual(node.to_html(), "This is plain text.")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Big Title")
        self.assertEqual(node.to_html(), "<h1>Big Title</h1>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Inline text")
        self.assertEqual(node.to_html(), "<span>Inline text</span>")

    def test_leaf_to_html_raises_value_error_when_value_empty(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", "")
            node.to_html()

    def test_valid_parentnode_creation(self):
        child1 = LeafNode(tag="span", value="Hello")
        child2 = "World"
        parent = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.tag, "div")
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0], child1)
        self.assertEqual(parent.children[1], child2)

    def test_invalid_tag(self):
        with self.assertRaises(ValueError):
            # Invalid tag (empty string)
            ParentNode(tag="", children=["Child content"])

        with self.assertRaises(ValueError):
            # Invalid tag (contains special characters)
            ParentNode(tag="123invalid", children=["Some child"])

    def test_empty_children_list(self):
        with self.assertRaises(ValueError):
            # No children provided
            ParentNode(tag="div", children=[])

    def test_invalid_children_type(self):
        with self.assertRaises(ValueError):
            # Children is not a list
            ParentNode(tag="div", children="Not a list")

        with self.assertRaises(TypeError):
            # Invalid type inside the children
            ParentNode(tag="div", children=["Valid string", 123])

    def test_to_html_with_valid_children(self):
        child1 = LeafNode(tag="p", value="Paragraph")
        child2 = "Plain text"
        child3 = LeafNode(tag="a", value="Click me", props={"href": "http://example.com"})

        parent = ParentNode(tag="div", children=[child1, child2, child3])
        expected_html = (
            '<div>'
            '<p>Paragraph</p>'
            'Plain text'
            '<a href="http://example.com">Click me</a>'
            '</div>'
        )
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_escapes_string_children(self):
        child = "<script>alert('XSS')</script>"
        parent = ParentNode(tag="div", children=[child])
        expected_html = (
            '<div>&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;</div>'
        )
        self.assertEqual(parent.to_html(), expected_html)

    def test_props_handling(self):
        child = LeafNode(tag="span", value="Child text")
        parent = ParentNode(tag="div", children=[child], props={"class": "container", "id": "main"})

        expected_html = '<div class="container" id="main"><span>Child text</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_empty_props(self):
        child = LeafNode(tag="span", value="Child text")
        parent = ParentNode(tag="div", children=[child])

        expected_html = '<div><span>Child text</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_htmlnode_inheritance(self):
        # Ensuring ParentNode maintains compatibility with functions expecting HTMLNode
        html_node = ParentNode(tag="section", children=["Some content"])
        self.assertIsInstance(html_node, HTMLNode)


if __name__ == "__main__":
    unittest.main()

