import os

from htmlnode import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(
        f"**** Generating page from {from_path} to {dest_path} usning {template_path}. ****"
    )
    with open(from_path, 'r') as f1:
        page_content = f1.read()
    with open(template_path, 'r') as f2:
        template = f2.read()
    html_content = markdown_to_html_node(page_content).to_html()
    title = extract_title(page_content)
    replced_title_template = template.replace("{{ Title }}", title)
    replced_title_content = replced_title_template.replace("{{ Content }}", html_content)
    directory = os.path.dirname(dest_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, 'w') as f3:
        f3.write(replced_title_content)
    