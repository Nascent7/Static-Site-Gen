from block_markdown import BlockType, markdown_to_blocks, block_to_block_type


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag                  # string representing HTML tag name "p", "a", "h1"
        self.value = value              # string representing value of HTML tag
        self.children =  children       # list of HTMLNode objs representing children on node
        self.props = props              # Dict of key-value pairs rep. atributes of HTML tag: ex. link <a> might have {"href":"https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        list_of_strings = []
        if self.props is not None:
            for i in self.props:
                list_of_strings.append(f' {i}="{self.props[i]}"')
            con_cat_strings = "".join(list_of_strings)
            return con_cat_strings
        else:
            return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError('A "tag" value is required. usage: "p", "b", "h1"')
        if self.children is None:
            raise ValueError('"Children" value is required. Argument expects a list.')
        if not isinstance(self.children, list):
            raise TypeError("Children must be of type list.")
        else:
            converted_list = []
            for i in self.children:
                converted_list.append(i.to_html())
            final_string = "".join(converted_list)
            return f'<{self.tag}{self.props_to_html()}>{final_string}</{self.tag}>'
        

# ---- The start of helper functions for markdown_to_html_node() ----

# Starts with most specific prefix first to avoid accidentally
# catching the wrong prefix.        
def heading_block_to_htmlNode(md_block):
    if md_block[1] == BlockType.HEADING:
        if md_block[0].startswith("###### "):
            h6_text = md_block[0].removeprefix("###### ")
            return LeafNode("h6", h6_text)
        if md_block[0].startswith("##### "):
            h5_text = md_block[0].removeprefix("##### ")
            return LeafNode("h5", h5_text)
        if md_block[0].startswith("#### "):
            h4_text = md_block[0].removeprefix("#### ")
            return LeafNode("h4", h4_text)
        if md_block[0].startswith("### "):
            h3_text = md_block[0].removeprefix("### ")
            return LeafNode("h3", h3_text)
        if md_block[0].startswith("## "):
            h2_text = md_block[0].removeprefix("## ")
            return LeafNode("h2", h2_text)
        if md_block[0].startswith("# "):
            h1_text = md_block[0].removeprefix("# ")
            return LeafNode("h1", h1_text)
        
def code_block_to_htmlNode(md_block):
    if md_block[1] == BlockType.CODE:
        stripped_prefix = md_block[0].removeprefix("```\n")
        final_text = stripped_prefix.removesuffix("```")
        return ParentNode("pre", [LeafNode("code", final_text)])

def quote_block_to_htmlNode(md_block):
    list_of_quote_lines = []
    if md_block[1] == BlockType.QUOTE:
        split_quote_lines = md_block[0].splitlines()
        for line in split_quote_lines:
            if not line.startswith(">"):
                raise Exception("Invalid markdown block quote format.")
            quote_line = line[1:].strip()
            list_of_quote_lines += text_to_children(quote_line)
        return ParentNode("blockquote", list_of_quote_lines)

# MD text supports multiple unordered list markers (ex.'*', '-')
# filtering for multiple markers in one check, to avoid issues with 
# lists that use mixed marker types.
def unordList_block_to_htmlNode(md_block):
    list_of_nodes = []
    if md_block[1] == BlockType.UNORD_LIST:
        split_unord_list = md_block[0].splitlines()
        for item in split_unord_list:
            if item.startswith("- "):
                unord_item = item.removeprefix("- ")
                list_of_nodes.append(ParentNode("li", text_to_children(unord_item)))
            elif item.startswith("* "):
                unord_item = item.removeprefix("* ")
                list_of_nodes.append(ParentNode("li", text_to_children(unord_item)))
            else:
                raise Exception("Invalid markdown unordered list format")
        return ParentNode("ul", list_of_nodes)

def ordList_block_to_htmlNode(md_block):
    list_of_nodes = []
    if md_block[1] == BlockType.ORD_LIST:
        split_ord_list = md_block[0].splitlines()
        counter = 1
        for item in split_ord_list:
            if item.startswith(f"{counter}. "):
                ord_item = item.removeprefix(f"{counter}. ")
                counter += 1
                list_of_nodes.append(ParentNode("li", text_to_children(ord_item)))
            else:
                raise Exception("Ivalid markdown ordered list format.")
        return ParentNode("ol", list_of_nodes)

# A helper function to make html nodes of the lists created by the unordered,
# ordered list, and paragraph types to node functions.
def text_to_children(text):
    from textnode import text_to_textnode, text_node_to_html_node
    text_nodes = text_to_textnode(text)
    html_node_list = []
    for node in text_nodes:
        convert_nodes = text_node_to_html_node(node)
        html_node_list.append(convert_nodes)
    return html_node_list

def paragraph_block_to_htmlNode(md_block):
    list_of_html_text_lines = []
    if md_block[1] == BlockType.PARAGRAPH:
        replaced_plain_lines = md_block[0].replace("\n", " ")
        list_of_html_text_lines.extend(text_to_children(replaced_plain_lines))
        return ParentNode("p", list_of_html_text_lines)


# Actual function to convert markdown to html nodes
# utilizing the helper functions above.
def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_children = []
    for block in md_blocks:
        md_block_type = block_to_block_type(block)
        # print("BLOCK:", repr(block[:60]), "TYPE:", md_block_type) # debug
        content_and_type = (block, md_block_type)
        if content_and_type[1] == BlockType.CODE:
            html_children.append(code_block_to_htmlNode(content_and_type))
        if content_and_type[1] == BlockType.HEADING:
            html_children.append(heading_block_to_htmlNode(content_and_type))
        if content_and_type[1] == BlockType.ORD_LIST:
            html_children.append(ordList_block_to_htmlNode(content_and_type))
        if content_and_type[1] == BlockType.UNORD_LIST:
            html_children.append(unordList_block_to_htmlNode(content_and_type))
        if content_and_type[1] == BlockType.QUOTE:
            html_children.append(quote_block_to_htmlNode(content_and_type))
        if content_and_type[1] == BlockType.PARAGRAPH:
            html_children.append(paragraph_block_to_htmlNode(content_and_type))
    return ParentNode("div", html_children)


# -------------------------------------

def extract_title(markdown):
    heading_found = False
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            cleaned_heading = line.strip()
            removed_prefix = cleaned_heading.removeprefix("# ")
            heading_found = True
            break
    if heading_found == True:
        return removed_prefix
    else:
        raise Exception("Missing H1 heading.")
