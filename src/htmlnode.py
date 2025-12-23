
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