import os
from blocktype import markdown_to_html_node
from extract_tag import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()


    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template_content.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for root, _, files in os.walk(dir_path_content):
        # Calculate the relative path of the current directory
        relative_path = os.path.relpath(root, dir_path_content)
        # Construct the destination directory path
        dest_subdir = os.path.join(dest_dir_path, relative_path)

        for file_name in files:
            # Process only markdown files
            if file_name.endswith(".md"):
                from_path = os.path.join(root, file_name)
                dest_path = os.path.join(dest_subdir, file_name[:-3] + ".html")  # Replace .md with .html
                generate_page(from_path, template_path, dest_path)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title found")
