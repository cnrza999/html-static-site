from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\)]+)\)')

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0

        for match in link_pattern.finditer(text):
            start, end = match.span()
            link_text = match.group(1)
            link_url = match.group(2)

            # Add preceding text as a normal text node
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            # Add the matched link as a link node
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            # Update the last processed index
            last_index = end

        # Add remaining text as a normal text node
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    image_pattern = re.compile(r'!\[([^\]]*)\]\((https?://[^\)]+)\)')  # Matches ![alt](url))

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

    text = node.text
    last_index = 0

    for match in image_pattern.finditer(text):
        start, end = match.span()
        alt_text = match.group(1)
        image_url = match.group(2)

        # Add preceding text as a normal text node
        if start > last_index:
            new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

        # Add the matched image as an image node
        new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

        # Update the last processed index
        last_index = end

    # Add remaining text as a normal text node
    if last_index < len(text):
        new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

