from gencontent import generate_page
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def delete_directory(directory_path):
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
    delete_directory(dir_path_public)
    copy_static_files(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_public, "index.html")
    )

# Call the main function when the script runs
if __name__ == "__main__":
    main()