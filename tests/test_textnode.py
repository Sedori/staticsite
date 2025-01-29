import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test", TextType.BOLD)
        node2 = TextNode("This is a test", TextType.ITALIC)
        node3 = TextNode("This is a test", TextType.BOLD)
        node4 = TextNode("Meme", TextType.TEXT, None)
        node5 = TextNode("What if it's broken?", "Meme", "https://segs.com")


        self.assertEqual(node, node3)
        self.assertNotEqual(node2, node)
        self.assertNotEqual(node3, node2)
        self.assertNotEqual(node5, node4)

if __name__ == "__main__":
    unittest.main()
