from gencontent import generate_page, generate_pages_recursive
import os
import shutil
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"


def delete_directory(directory_path):
    print("Deleting public directory...")
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path) # Delete all
        print(f"Deleting public directory: {directory_path}")
    else:
        print(f"Directory does not exist: {directory_path}")

def copy_static_files(static_dir, public_dir):
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)
        print(f"Copied static files from {static_dir} to {public_dir}")
    else:
        print(f"Static directory does not exist: {static_dir}")


def main():
    # Determine the base path from the CLI argument. If not detault to "/".
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"


    delete_directory(dir_path_public)
    copy_static_files(dir_path_static, dir_path_public)

    print("Generating page...")

    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

# Call the main function when the script runs
if __name__ == "__main__":
    main()