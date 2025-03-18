import re
import html

VALID_TAG_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$")

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        if not self.tag:
            raise ValueError("HTMLNode must have a non-empty tag.")

        if self.children is None:
            raise ValueError("HTMLNode must have children defined (even if empty).")

        # Process children recursively
        children_html = "".join(
            child.to_html() if isinstance(child, HTMLNode) else str(child)
            for child in self.children
        )

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(
        f'{key.strip()}="{value.strip()}"' if not isinstance(value, bool) else f'{key.strip()}' for key, value in self.props.items()
    )

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={len(self.children)} children, props={self.props!r})"
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a non-empty value.")

        if self.tag is None:
            return self.value

        # Render HTML with props and tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag or not VALID_TAG_RE.match(tag):
            raise ValueError("ParentNode must have a valid HTML tag name (e.g., letters and digits only).")
        if not children or not isinstance(children, list):
            raise ValueError("ParentNode must have at least one child and children must be a list.")
        for child in children:
            if not isinstance(child, (HTMLNode, str)):
                raise TypeError("All children of ParentNode must be either HTMLNode instances or strings.")
        super().__init__(tag=tag, children=children, props=props or {})

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a non-empty tag.")
        children_html = "".join(
            child.to_html() if isinstance(child, HTMLNode) else html.escape(str(child))
            for child in self.children
        )
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    
