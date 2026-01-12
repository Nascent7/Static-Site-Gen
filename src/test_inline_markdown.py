import unittest

from inline_markdown import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodeLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and a [link](https://www.youtube.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is text with no links", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with no links", TextType.PLAIN)], new_nodes)

    def test_split_type_link(self):
        node = TextNode("link", TextType.LINK, "https://www.somelink.com")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://www.somelink.com")], new_nodes)

    def test_split_multi_links_not_seperated(self):
        node = TextNode(
            "This is text before two links [link1](https://www.somelink1.com)[link2](https://www.somelink2.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text before two links ", TextType.PLAIN),
                TextNode("link1", TextType.LINK, "https://www.somelink1.com"),
                TextNode("link2", TextType.LINK, "https://www.somelink2.com"),
            ],
            new_nodes,
        )

    def test_split_link_first(self):
        node = TextNode("[link](https://www.somelink.com) with text following", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.somelink.com"),
                TextNode(" with text following", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_link_multi_nodes_plain(self):
        node = [
            TextNode("Some text [link1](www.somelink1.com) some following text", TextType.PLAIN),
            TextNode("More text [link2](www.somelink2.com) more following text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("Some text ", TextType.PLAIN),
                TextNode("link1", TextType.LINK, "www.somelink1.com"),
                TextNode(" some following text", TextType.PLAIN),
                TextNode("More text ", TextType.PLAIN),
                TextNode("link2", TextType.LINK, "www.somelink2.com"),
                TextNode(" more following text", TextType.PLAIN),
            ],
            new_nodes,
        )


class TestSplitNodeImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/someid.png) and another ![second image](https://i.imgur.com/anotherid.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/someid.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/anotherid.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text with no images", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with no images", TextType.PLAIN)], new_nodes)

    def test_split_type_image(self):
        node = TextNode("image", TextType.IMAGE, "https://www.someimage.com/someid.jpg")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://www.someimage.com/someid.jpg")], new_nodes)

    def test_split_multi_images_not_seperated(self):
        node = TextNode(
            "This is text before two images ![alttext1](https://www.someimage1.com/image1.png)![alttext2](www.someimage2.com/image2.jpg)",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text before two images ", TextType.PLAIN),
                TextNode("alttext1", TextType.IMAGE, "https://www.someimage1.com/image1.png"),
                TextNode("alttext2", TextType.IMAGE, "www.someimage2.com/image2.jpg")
            ],
            new_nodes,
        )
    def test_split_image_first(self):
        node = TextNode("![alt](https://www.someimage.com/someid.png) with text following", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://www.someimage.com/someid.png"),
                TextNode(" with text following", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_split_image_multi_nodes_plain(self):
        node = [
            TextNode("Some text ![alt1](www.someimage1.com/image1.png) some following text", TextType.PLAIN),
            TextNode("More text ![alt2](www.someimage2.com/image2.png) more following text", TextType.PLAIN),
        ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("Some text ", TextType.PLAIN),
                TextNode("alt1", TextType.IMAGE, "www.someimage1.com/image1.png"),
                TextNode(" some following text", TextType.PLAIN),
                TextNode("More text ", TextType.PLAIN),
                TextNode("alt2", TextType.IMAGE, "www.someimage2.com/image2.png"),
                TextNode(" more following text", TextType.PLAIN),
            ],
            new_nodes,
        )

class TestSplitNodeLinkImage(unittest.TestCase):
    def test_split_link_split_image(self):
        node = TextNode("text [link](www.somelink.com) more text ![image](www.someimge.com/image.png)", TextType.PLAIN)
        new_node = split_nodes_image(split_nodes_link([node]))
        self.assertListEqual(
            [
                TextNode("text ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "www.somelink.com"),
                TextNode(" more text ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "www.someimge.com/image.png"),
            ],
            new_node,
        )

    def test_split_link_split_image_muliple(self):
        node = [
            TextNode("text [link](www.somelink.com) more text ![image](www.someimge.com/image.png)", TextType.PLAIN),
            TextNode("text ![image](www.someimge.com/image.png) more text [link](www.somelink.com)", TextType.PLAIN)
        ]
        new_node = split_nodes_image(split_nodes_link(node))
        self.assertListEqual(
            [
                TextNode("text ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "www.somelink.com"),
                TextNode(" more text ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "www.someimge.com/image.png"),
                TextNode("text ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "www.someimge.com/image.png"),
                TextNode(" more text ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "www.somelink.com"),
            ],
            new_node,
        )


class TestSplitNodeImageLink(unittest.TestCase):
    def test_split_image_split_link(self):
        node = TextNode("text ![image](www.someimge.com/image.png) more text [link](www.somelink.com)", TextType.PLAIN)
        new_node = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("text ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "www.someimge.com/image.png"),
                TextNode(" more text ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "www.somelink.com"),
            ],
            new_node,
        )

    def test_split_image_split_link_multiple(self):
        node = [
            TextNode("text ![image](www.someimge.com/image.png) more text [link](www.somelink.com)", TextType.PLAIN),
            TextNode("text [link](www.somelink.com) more text ![image](www.someimge.com/image.png)", TextType.PLAIN)
        ]
        new_node = split_nodes_link(split_nodes_image(node))
        self.assertListEqual(
            [
                TextNode("text ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "www.someimge.com/image.png"),
                TextNode(" more text ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "www.somelink.com"),
                TextNode("text ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "www.somelink.com"),
                TextNode(" more text ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "www.someimge.com/image.png"),
            ],
            new_node,
        )


if __name__ == "__main__":
    unittest.main()