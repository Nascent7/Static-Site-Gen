from enum import Enum

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
