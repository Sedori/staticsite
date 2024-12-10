import unittest
from blocknode import markdown_to_blocks, block_to_block_type

class TestMarkdownBlocks(unittest.TestCase):
    def test_basic_blocks(self):
        markdown = """# Header

This is a paragraph.

* List item 1
* List item 2
* List item 3

This is a second paragraph
Sike it's also a list"""
        
        expected = ["# Header", "This is a paragraph.", "* List item 1\n* List item 2\n* List item 3", "This is a second paragraph\nSike it's also a list"]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_block_to_block(self):
        markdown = """# Header

This should be a paragraph.

- List 1
* List 2
- List 3

1. What
2. The
3. Heck

> Green Text LMAO
> Meow
> What

``` Code Block
Shouldn't code blocks be bigger ```

###### Header

##### Header

"""

        blocks = markdown_to_blocks(markdown)
        blocklist = []
        for block in blocks:
            blocklist.append(block_to_block_type(block))

        expected = ["heading", "paragraph", "ulist", "olist",
                "block", "code", "heading", "heading"]

        self.assertEqual(blocklist, expected)


if __name__ == '__main__':
    unittest.main()
