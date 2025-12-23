import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.LINK, "www.boot.dev/dashboard")
        node4 = TextNode("This is a text node", TextType.LINK, "www.boot.dev/dashboard")
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        node3 = TextNode("This is a text node", TextType.LINK, "www.boot.dev/dashboard")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
    
    def test_urlNone(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        node3 = TextNode("This is a text node", TextType.LINK, "www.boot.dev/dashboard")
        node4 = TextNode("This is a text node", TextType.LINK, "www.boot.dev/dashboard")
        node5 = TextNode("This is a text node", TextType.BOLD, "www.boot.dev/dashboard")
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node5)

    def test_url(self):
        node = TextNode("This is a text node", TextType.PLAIN, None)
        node2 = TextNode("This is a text node", TextType.PLAIN, "www.boot.dev/dashboard")
        self.assertNotEqual(node, node2)
    
    def test_textnoteq(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a different text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_typenoteq(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is text", TextType.LINK,"www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is text")
        self.assertEqual(html_node.props, {"href":"www.boot.dev"})

    def test_img(self):
        node = TextNode("This is text", TextType.IMAGE,"www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props,{"src":"www.boot.dev", "alt":"This is text"})


if __name__ == "__main__":
    unittest.main()