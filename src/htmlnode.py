from textnode import TextNode, TextType
from splitnode import split_nodes_link, split_nodes_image, split_nodes_delimiter

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be an instance of TextNode")

    if text_node.text_type == TextType.TEXT:
        # No tag, just raw text
        return LeafNode(tag=None, value=text_node.text)

    elif text_node.text_type == TextType.BOLD:
        # "b" tag with text
        return LeafNode(tag="b", value=text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        # "i" tag with text
        return LeafNode(tag="i", value=text_node.text)

    elif text_node.text_type == TextType.CODE:
        # "code" tag with text
        return LeafNode(tag="code", value=text_node.text)

    elif text_node.text_type == TextType.LINK:
        # "a" tag with text and "href" prop
        if not text_node.url:
            raise ValueError("TextNode of type LINK must have a URL")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        # "img" tag with "src" and "alt" props
        if not text_node.url:
            raise ValueError("TextNode of type IMAGE must have a URL for 'src'")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})

    else:
        # Raise an error for unsupported TextType
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def text_to_textnodes(text):
    # Initialize the text as a single text node
    nodes = [TextNode(text, TextType.TEXT)]

    # Use each split function one after the other
    nodes = split_nodes_image(nodes)  # Process images
    nodes = split_nodes_link(nodes)  # Process links
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # Process bold text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # Process italic text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # Process code blocks

    return nodes