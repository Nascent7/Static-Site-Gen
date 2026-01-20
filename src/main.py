import os
import shutil

from textnode import TextNode
from textnode import TextType
from copystatic import copy_static
from generatepage import generate_pages_recursive


def main():
        # sample = "Some text"
        # text_fmt = TextType.BOLD
        # print(TextNode(sample, text_fmt))

        if os.path.exists("public"):
                shutil.rmtree("public")
        os.mkdir("public")
        copy_static("static", "public")

        # generate_page("content/index.md","template.html", "public/index.html")
        generate_pages_recursive("content", "template.html", "public")
main()