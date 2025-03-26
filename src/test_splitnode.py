import unittest
from splitnode import (
    split_nodes_delimiter, split_nodes_link, split_nodes_image
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode("Visit [Google](https://google.com) and [Python](https://www.python.org).", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Python", TextType.LINK, "https://www.python.org"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is a text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("This is a text with no links.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_nodes_image(self):
        node = TextNode("This contains an image ![alt text](https://example.com/image.png).", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This contains an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is a text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [TextNode("This is a text with no images.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_nodes_combined(self):
        node = TextNode(
            "Here is ![an image](https://example.com/image.jpg) and [a link](https://example.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])  # Split images first
        new_nodes = split_nodes_link(new_nodes)  # Then split links

        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "https://example.com/image.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
