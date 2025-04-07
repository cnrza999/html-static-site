import unittest

from blocktype import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = """
    This is **bolded** paragraph.

    This is another paragraph with _italic_ text and `code` here.
    This is the same paragraph on a new line.

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph.",
                "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        """Test when the input is empty."""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_line(self):
        """Test when the input is a single line."""
        md = "This is a single line of Markdown."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line of Markdown."])

    def test_markdown_to_blocks_multiple_paragraphs(self):
        """Test when the input has multiple paragraphs."""
        md = """
    Paragraph one.

    Paragraph two.

    Paragraph three.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph one.",
                "Paragraph two.",
                "Paragraph three.",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        """Test when the input has excessive newlines."""
        md = """
    Paragraph one.






    Paragraph two.



    Paragraph three.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph one.",
                "Paragraph two.",
                "Paragraph three.",
            ],
        )

    def test_markdown_to_blocks_heading_and_list(self):
        """Test Markdown with a mix of headings, paragraphs, and lists."""
        md = """
    # Heading

    This is a paragraph.

    - List item 1
    - List item 2
    - List item 3

    Another paragraph.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph.",
                "- List item 1\n- List item 2\n- List item 3",
                "Another paragraph.",
            ],
        )

    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "### Subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "###### Small heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ndef func():\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "```\nJust some code here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "> Line 1 in a quote\n> Line 2 in the same quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1. Only one item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "Some text that doesn't match any other type."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_paragraph(self):
            md = """
    This is **bolded** paragraph
    text in a p
    tag here

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
            )

        def test_paragraphs(self):
            md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_lists(self):
            md = """
    - This is a list
    - with items
    - and _more_ items

    1. This is an `ordered` list
    2. with items
    3. and more items

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
            )

        def test_headings(self):
            md = """
    # this is an h1

    this is paragraph text

    ## this is an h2
    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
            )

        def test_blockquote(self):
            md = """
    > This is a
    > blockquote block

    this is paragraph text

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
            )

        def test_code(self):
            md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )



if __name__ == "__main__":
    unittest.main()