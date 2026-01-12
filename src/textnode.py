from enum import Enum

from htmlnode import LeafNode



class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):    # Is comapring the different values 
        return (
            self.text == other.text and
            self.text_type == other.text_type and 
            self.url == other.url
        )

    def __repr__(self):     # .value will print "Bold" insted of TextType.BOLD when printing the TextNode object
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    else:
        raise Exception("Not an accepted text type.")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    not_plain = []
    if delimiter == "":
        return old_nodes
    for old_node in old_nodes:
        if old_node.text_type is not TextType.PLAIN:
            not_plain.append(old_node)
        else:
            split_nodes = []
            new_text = old_node.text.split(delimiter)
            if len(new_text) % 2 == 0 and len(new_text) > 1:
                raise ValueError("Invalid Markdown syntax. Missing a closing delimiter.")
            for i in range (len(new_text)):
                if new_text[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(new_text[i], TextType.PLAIN))
                else:
                    split_nodes.append(TextNode(new_text[i], text_type))
            not_plain.extend(split_nodes)
    return not_plain


def text_to_textnode(text):
    from inline_markdown import split_nodes_image, split_nodes_link
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    