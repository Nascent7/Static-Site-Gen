import os

from htmlnode import markdown_to_html_node, extract_title
from pathlib import Path


# def generate_page(from_path, template_path, dest_path):
#     print(
#         f"**** Generating page from {from_path} to {dest_path} usning {template_path}. ****"
#     )
#     with open(from_path, 'r') as f1:
#         page_content = f1.read()
#     with open(template_path, 'r') as f2:
#         template = f2.read()
#     html_content = markdown_to_html_node(page_content).to_html()
#     title = extract_title(page_content)
#     replced_title_template = template.replace("{{ Title }}", title)
#     replced_title_content = replced_title_template.replace("{{ Content }}", html_content)
#     directory = os.path.dirname(dest_path)
#     if directory:
#         os.makedirs(directory, exist_ok=True)
#     with open(dest_path, 'w') as f3:
#         f3.write(replced_title_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_path = Path(dir_path_content)
    dest_path = Path(dest_dir_path)
    for entry in os.listdir(dir_path_content):
        full_entry_path = content_path / Path(entry)

        if full_entry_path.is_file():
            relative_path = full_entry_path.relative_to(content_path)  #removes current directory
            html_relative = relative_path.with_suffix(".html")
            final_path = dest_path / html_relative

            with open(full_entry_path, 'r') as f1:
                page_content = f1.read()
            with open(template_path) as f2:
                template = f2.read()

            html_content = markdown_to_html_node(page_content).to_html()
            title = extract_title(page_content)
            replced_title_template = template.replace("{{ Title }}", title)
            replced_title_content = replced_title_template.replace("{{ Content }}", html_content)
            final_path.parent.mkdir(parents=True, exist_ok=True)
            with open(final_path, 'w') as f3:
                f3.write(replced_title_content)

        else:
            sub_dest = dest_path / entry
            generate_pages_recursive(full_entry_path, template_path, sub_dest)


