from enum import Enum


def markdown_to_blocks(text):
    if text == "":
        return [text]
    lines = text.splitlines()
    blocks = []
    current_block_lines = [] # Hold lines for the block being currently built
    for line in lines:
        stripped_line = line.strip() # Removes white space for each line
        if stripped_line == "": 
            if current_block_lines:
                blocks.append("\n".join(current_block_lines))
            current_block_lines = []
        else:
            current_block_lines.append(stripped_line)
    # Cleaning up a block that wasn't terminated by an empty line
    if current_block_lines:
        blocks.append("\n".join(current_block_lines))
    filtered_blocks = list(filter(lambda x: x != "", blocks)) # Finally, filter out any blocks that might still be empty
    return filtered_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD_LIST = "unordered list"
    ORD_LIST = "ordered list"

def block_to_block_type(md_block):
    if md_block.startswith(('# ','## ','### ','#### ','##### ', '###### ')):
        return BlockType.HEADING
    if md_block.startswith('```\n') and md_block.endswith('```'):
        return BlockType.CODE
    if md_block.startswith(">"):
        sep_line = md_block.splitlines()
        for line in sep_line:
            if line.startswith('>'):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if md_block.startswith('- ') or md_block.startswith('* '):
        split_unord_lines = md_block.splitlines()
        for item in split_unord_lines:
            if item.startswith('- ') or item.startswith('* '):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORD_LIST
    # Starting Ordered list check by assuming the block may be an ordered list since no
    # other BlockType has matched. Prceeding through attempting to prove the assumption false.
    split_ord_list = md_block.splitlines()
    is_ord_list = True
    # Using enumerate to get line_num if needed for debugging, though not strictly for logic here
    # Adds a counter to an iterable and returns an enumerate object, which yields pairs of (index, item) 
    # in each iteration. This would allow for enforcement of stricter ordered list rules.
    for line_num, line in enumerate(split_ord_list):
        dot_pos = line.find('.')
        if dot_pos == -1: # must have dot. -1 is the result if the parameter is missing.
            is_ord_list = False
            break
        if not line[0:dot_pos].isdigit(): #Characters before the dot must be digits
            is_ord_list = False
            break
        if not (dot_pos + 1 < len(line) and line[dot_pos + 1] == ' '): # Must be followed by a space after the dot
            is_ord_list = False
            break
    if is_ord_list == True:
        return BlockType.ORD_LIST
    else:
        return BlockType.PARAGRAPH