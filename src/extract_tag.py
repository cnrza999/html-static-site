import re
import os
from blocktype import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 header found in the markdown text.")

def generate_page(from_path, dest_path, template_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as markdown_file:
        markdown_content = markdown_file.read()

    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title from the markdown
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    generated_content = template_content.replace("{{ Title }}", title)
    generated_content = generated_content.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the generated HTML to the destination path
    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(generated_content)