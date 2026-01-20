import os

from htmlnode import markdown_to_html_node, extract_title
from pathlib import Path


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"**** Generating page from {from_path} to {dest_path} using {template_path}. ****"
    )
    with open(from_path, 'r') as f1:
        page_content = f1.read()
    with open(template_path, 'r') as f2:
        template = f2.read()
    html_content = markdown_to_html_node(page_content).to_html()
    title = extract_title(page_content)
    replaced_title_template = template.replace("{{ Title }}", title)
    replaced_title_content = replaced_title_template.replace("{{ Content }}", html_content)
    replaced_content = replaced_title_content.replace(
        'href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}'
    )
    directory = os.path.dirname(dest_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, 'w') as f3:
        f3.write(replaced_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
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
            replaced_title_template = template.replace("{{ Title }}", title)
            replaced_title_content = replaced_title_template.replace("{{ Content }}", html_content)
            replaced_content = replaced_title_content.replace(
                'href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}'
            )
            final_path.parent.mkdir(parents=True, exist_ok=True)
            with open(final_path, 'w') as f3:
                f3.write(replaced_content)

        else:
            sub_dest = dest_path / entry
            generate_pages_recursive(full_entry_path, template_path, sub_dest, basepath)
