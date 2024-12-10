import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, extract_title
from textnode import TextType, TextNode

class TestHTMLNode(unittest.TestCase):
    def test_for_eq_attribs(self):
        html_dict = {
                "href": "https://www.google.com",
                "target": "_blank",
            }

        expected = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=html_dict)
        self.assertEqual(node.props_to_html(), expected)

    def test_for_no_attribs(self):
        html_dict = {}
        expected = ''
        node = HTMLNode(props=html_dict)
        self.assertEqual(node.props_to_html(), expected)

    def test_for_none_attribs(self):
        html_dict = None
        expected = ''
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), expected)

    def test_for_leaf_without_props(self):
        html_dict = {}
        expected = "<p>This is a paragraph of text.</p>"
        node = LeafNode("p", "This is a paragraph of text.", html_dict)
        self.assertEqual(node.to_html(), expected)

    def test_for_leaf_with_props(self):
        html_dict = {"href": "https://www.google.com"}
        expected = '<a href="https://www.google.com">Click me!</a>'
        node = LeafNode("a", "Click me!", html_dict)
        self.assertEqual(node.to_html(), expected)

    def test_for_leaf_with_no_tags(self):
        node = LeafNode(None, "Meows")
        expected = "Meows"
        self.assertEqual(node.to_html(), expected)

    def test_for_value_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_basic_parent(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "Italic text")
        parent_node = ParentNode(
                "p",
                [leaf1, leaf2, leaf3]
        )
        
        expected = "<p><b>Bold text</b>Normal text<i>Italic text</i></p>"

        self.assertEqual(parent_node.to_html(), expected)

    def internal_parent(self):
        leaf1 = LeafNode("b", "Benis Text")
        leaf2 = LeafNode("u", "Yuri Text")
        leaf3 = LeafNode("i", "Ice Cream Text")
        
        inner_node = ParentNode(
                "h1",
                [leaf2, leaf3]
        )
        outer_node = ParentNode(
                "p",
                [leaf1, inner_node, leaf3]
        )
        
        expected = "<p><b>Benis Text</b><h1><u>Yuri Text</u><i>Ice Cream Text</i></h1><i>Ice Cream Text</i></p>"

        self.assertEqual(outer_node.to_html(), expected)

    def test_incorrect_children_parent(self):
        with self.assertRaises(TypeError):
            node = ParentNode("p", "LMAO")
            node.to_html()  
    
    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("v", [])
            node.to_html()

    def test_literally_no_children_not_even_an_argument(self):
        with self.assertRaises(TypeError):
            node = ParentNode("benis")
            node.to_html()

    def test_for_textnode_to_htmlnode_images(self):
        text_node = TextNode("This is a Meow", TextType.IMAGE, "meme.jpeg")
        html_node = text_node_to_html_node(text_node)
        
        expected = '<img src="meme.jpeg" alt="This is a Meow">'

        self.assertEqual(html_node.to_html(), expected)

    def test_for_regular_text_but_with_url_for_some_reason(self):
        text_node = TextNode("Wow do it again", TextType.TEXT, "I'm just here URL")
        html_node = text_node_to_html_node(text_node)

        expected = "Wow do it again"
        self.assertEqual(html_node.to_html(), expected)

    def test_for_bold_text(self):
        text_node = TextNode("I'm emboldened", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        expected = "<b>I'm emboldened</b>"
        self.assertEqual(html_node.to_html(), expected)

    def test_for_italics(self):
        text_node = TextNode("I'm Italian", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        expected = "<i>I'm Italian</i>"
        self.assertEqual(html_node.to_html(), expected)

    def test_for_code(self):
        text_node = TextNode("I'm not Code", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        expected = "<code>I'm not Code</code>"
        self.assertEqual(html_node.to_html(), expected)

    def test_for_link(self):
        text_node = TextNode("I'm LINK", TextType.LINK, "https://im.url.com")
        html_node = text_node_to_html_node(text_node)

        expected = "<a href=\"https://im.url.com\">I\'m LINK</a>"
        self.assertEqual(html_node.to_html(), expected)

    def test_for_simple_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                   ]

        self.assertListEqual(new_nodes, expected)

    def test_for_missing_delimiter(self):
        node = TextNode("Hello `World", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        
        expected = [TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),]
        
        self.assertEqual(expected, new_nodes)

    def test_for_markdown_images(self):
        markdown = "This is a text with a link ![police camp](https://www.boot.dev) and ![meme](https://world.com)"
        expected = [('police camp', 'https://www.boot.dev'), ('meme', 'https://world.com')]

        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_two(self):
        markdown ="""## This shouldn't be the title
# Definitely not

# This should be the title, meow

# 2. This shouldn't be the title"""

        expected = "This should be the title, meow"
        self.assertEqual(extract_title(markdown), expected)

    def test_extract_exception(self):
        with self.assertRaises(Exception):
            extract_title("## This is h2\n### Technically still the same block")
        


if __name__ == "__main__":
    unittest.main()
