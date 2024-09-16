import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("a", "This is some information!", None, {"href": "https://www.google.com", "target": "_blank"})
        print(node)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is some information!", None, {"href": "https://www.google.com", "target": "_blank"})
        prop_string = node.props_to_html()
        self.assertEqual(prop_string, ' href="https://www.google.com" target="_blank"')

    def test_to_html_no_children(self):
        node = LeafNode("p", "I'm a paragraph!!!!")
        self.assertEqual(node.to_html(), "<p>I'm a paragraph!!!!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "I have no tag!")
        self.assertEqual(node.to_html(), "I have no tag!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()