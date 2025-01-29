import os
import shutil
from .htmlnode import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown_content = file.read()
        print("Raw markdown content:\n")
        #print(markdown_content)

    with open(template_path, 'r') as file:
        template_content = file.read()
        print("Template content:\n")
        #print(template_content)

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(final_html)

def generate_pages_recursive(from_path, template_path, dest_path):

    items = os.listdir(from_path)
    for item in items:

        source_item = os.path.join(from_path, item)
        if os.path.isfile(source_item):

            file_name, extension = os.path.splitext(item)
            print(f"Generating page from\n\n {source_item}\n\n to\n\n {dest_path}\n\n using {template_path}")
    
            with open(source_item, 'r') as file:
                markdown_content = file.read()
                #print(markdown_content)

            with open(template_path, 'r') as file:
                template_content = file.read()
                #print(template_content)

            html_node = markdown_to_html_node(markdown_content)
            html_content = html_node.to_html()
            title = extract_title(markdown_content)

            final_html = template_content.replace("{{ Title }}", title)
            final_html = final_html.replace("{{ Content }}", html_content)

            dir_path = os.path.dirname(dest_path)
            os.makedirs(dir_path, exist_ok=True)

            html_filename = os.path.join(dest_path, file_name + '.html')

            with open(html_filename, 'w') as file:
                file.write(final_html)
        
        else:
            new_dest = os.path.join(dest_path, item)
            os.mkdir(new_dest)
            generate_pages_recursive(source_item, template_path, new_dest)

def copy_static(source, dest):

    # deletes everything first

    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    # creates a fresh directory

    os.mkdir(dest)

    items = os.listdir(source)
    for item in items:
        source_item = os.path.join(source, item)
        if os.path.isfile(source_item):
            shutil.copy(source_item, dest)
            print(f"Copied {source_item} to {dest}")
        else:
            new_dest = os.path.join(dest, item)
            os.mkdir(new_dest)
            print(f"Created {new_dest}")
            copy_static(source_item, new_dest)


def list_files(source, dest):

    if not os.path.exists(dest):
        os.mkdir(dest)

    files = os.listdir(source)
    print("Files found in source directory:")
    for file in files:
        source_path = os.path.join(source, file)

        if os.path.isfile(source_path):
            print(file)


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    content_dir = os.path.join(project_root, "content")
    template_dir = os.path.join(project_root, "template.html")

    # copy static with source (static) and dest (public)
    copy_static(static_dir, public_dir)
    #generate_page(content_dir, template_dir, os.path.join(public_dir, "index.html"))
    #list_files("static", "public")
    generate_pages_recursive(content_dir, template_dir, public_dir) 

if __name__ == "__main__":
    main()
