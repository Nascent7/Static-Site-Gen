import os
import shutil
import sys

from textnode import TextNode
from textnode import TextType
from copystatic import copy_static
from generatepage import generate_pages_recursive, generate_page


def main():
        if len(sys.argv) == 1:
                basepath = "/"
        else:
                basepath = sys.argv[1]

        if os.path.exists("docs"):
                shutil.rmtree("docs")
        os.mkdir("docs")
        copy_static("static", "docs")

        generate_page("content/index.md","template.html", "docs/index.html", basepath)
        generate_pages_recursive("content", "template.html", "docs", basepath)
main()