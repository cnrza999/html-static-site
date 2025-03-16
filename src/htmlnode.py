class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("HTMLNode.to_html not implemented")

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
