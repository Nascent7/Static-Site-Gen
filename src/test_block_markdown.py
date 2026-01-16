import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type



class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_no_text(self):
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_heading(self):
        text = "### Heading 3 here"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, block_type)
    
    def test_block_to_quote(self):
        text = """> This is a quote of 
> some thing important 
> from some one of importance
"""
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_unord_list(self):
        text = """- this 
- is 
- an
- unordered list
"""
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.UNORD_LIST, block_type)

    def test_block_to_ord_list(self):
        text = """1. this 
2. is 
3. an
4. ordered list
"""
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.ORD_LIST, block_type)

    def test_block_to_code(self):
        text = """```
This is some code written here
wiht more code
    and more with 
        indentation
```"""
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_paragraph(self):
        text = "This is a plain paragraph with no fancy formatting"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, block_type)