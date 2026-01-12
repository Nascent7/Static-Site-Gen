from textnode import TextNode, TextType
from linknode import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                curr_text = node.text
                for alt, url in images:
                    pattern = f"![{alt}]({url})"
                    before, after = curr_text.split(pattern, 1)
                    if before != "":
                        new_nodes.append(TextNode(before, TextType.PLAIN))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    curr_text = after
                if curr_text != "":
                    new_nodes.append(TextNode(curr_text, TextType.PLAIN))
    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                curr_text = node.text
                for alt, url in links:
                    pattern = f"[{alt}]({url})"
                    before, after = curr_text.split(pattern, 1)
                    if before != "":
                        new_nodes.append(TextNode(before, TextType.PLAIN))
                    new_nodes.append(TextNode(alt, TextType.LINK, url))
                    curr_text = after
                if curr_text != "":
                    new_nodes.append(TextNode(curr_text, TextType.PLAIN))
    return new_nodes