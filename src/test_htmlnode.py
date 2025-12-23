import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            tag = None, 
            value = None, 
            children = None, 
            props = {
                "href":"https://www.google.com",
                "target":"_blank"
            }
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_propsnonne(self):
        node = HTMLNode(props = None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_propsempty(self):
        node = HTMLNode(props = {})
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold text")
        self.assertEqual(node.to_html(), "<b>This is bold text</b>")

    def test_leaf_to_html_none(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_leaf_to_html_val_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_wtihout_tag(self):
        child_node = LeafNode("b", "Bold")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_wtihout_children(self):
        parent_node = ParentNode("h1", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_wtihout_tag_message(self):
        child_node = LeafNode("b", "Bold")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as ctx:
            parent_node.to_html()
        self.assertEqual(str(ctx.exception),
                         'A "tag" value is required. usage: "p", "b", "h1"',
                         )

    def test_to_html_wtihout_children_message(self):
        parent_node = ParentNode("h1", None)
        with self.assertRaises(ValueError) as ctx:
            parent_node.to_html()
        self.assertEqual(str(ctx.exception),
                         '"Children" value is required. Argument expects a list.',
                         )

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "child 1")
        child_node2 = LeafNode("div", "child 2")
        child_node3 = LeafNode("p", "child 3")
        child_node4 = LeafNode("i", "child 4")
        parent_node = ParentNode("a", [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(), '<a><span>child 1</span><div>child 2</div><p>child 3</p><i>child 4</i></a>')

    def test_to_html_empty_list_children(self):
        parent_node = ParentNode("b", [])
        self.assertEqual(parent_node.to_html(), '<b></b>')

    def test_to_html_with_props(self):
        child_node = LeafNode("p", "plain text")
        parent_node = ParentNode("p", [child_node], {"class": "note", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<p class="note" id="main"><p>plain text</p></p>'
        )
    def test_to_html_text_cild_only(self):
        child_node = LeafNode(None, "raw text")
        parent_node = ParentNode("b", [child_node])
        self.assertEqual(parent_node.to_html(), "<b>raw text</b>")

    def test_to_html_children_not_list(self):
        parent_node = ParentNode("p", "Not a list")
        with self.assertRaises(TypeError) as ctx:
            parent_node.to_html()

    def test_to_html_children_not_list_message(self):
        parent_node = ParentNode("p", "Not a list")
        with self.assertRaises(TypeError) as ctx:
            parent_node.to_html()
        self.assertEqual(str(ctx.exception),
                         "Children must be of type list.",
                         )

    def test_to_html_nested_parents(self):
        child_node1 = LeafNode("b", "bold")
        child_node2 = LeafNode("i", "italic")
        child_node3 = LeafNode(None, "raw")
        parent_node1 = ParentNode("span",[child_node2])
        parent_node2 = ParentNode("div",[child_node1,parent_node1, child_node3])
        self.assertEqual(parent_node2.to_html(), '<div><b>bold</b><span><i>italic</i></span>raw</div>')

    def test_to_html_empty_string_child(self):
        child_node = LeafNode("p", "")
        parent_node = ParentNode("b", [child_node])
        self.assertEqual(parent_node.to_html(), "<b><p></p></b>")