import re

def extract_markdown_images(text):

    # images
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(pattern, text)

    return matches

def extract_markdown_links(text):

    # links
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(pattern, text)

    return matches
