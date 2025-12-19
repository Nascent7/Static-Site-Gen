from textnode import TextNode
from textnode import TextType

def main():
        sample = "Some text"
        text_fmt = TextType.BOLD
        print(TextNode(sample, text_fmt))
main()