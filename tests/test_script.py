from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, text_to_textnodes, markdown_to_html_node, extract_title
from blocknode import markdown_to_blocks, block_to_block_type


def old_main():
    node1 = TextNode("Hello", TextType.TEXT, "https://www.boot.dev")
    node2 = TextNode("Hi", TextType.BOLD, "https://www.boot.dev")
    node3 = TextNode("Hello", TextType.TEXT, "https://www.boot.dev")
    node4 = TextNode("World", TextType.ITALIC)
    node5 = TextNode("", TextType.IMAGE, "https://i.redd.it/br7gmy9hq24e1.jpg")
    
    node11 = LeafNode("img", "", {"src": "cat.jpg", "alt": "cute cat"})
    node12 = LeafNode("p", "Hello world")
    node13 = LeafNode(None, "Just some text")
    node14 = LeafNode("a", "Click me!", {"href": "https://example.com"})

    print("This is testing the LeafNodes")
    print(node11.to_html(), node12.to_html(), node13.to_html(), node14.to_html())

    print("This is for testing the text_node_to_html_node")
    print(LeafNode.to_html(text_node_to_html_node(node5)))


    print(node1)

    print(node1 == node2)
    print(node1 == node3)
    print(node3 == node4)

    html_dict = { "href": "https://www.google.com", "target": "_blank", }

    node_html1 = HTMLNode("Tag", "Value", "Children", html_dict)

    print(node_html1)

    print(HTMLNode.props_to_html(node_html1))

    print(LeafNode.to_html(node_html1))

    print("This is testing for the ParentNode")
    leaf1 = LeafNode("b", "Bold text")
    leaf2 = LeafNode(None, "Normal text")
    leaf3 = LeafNode("i", "Italic Text")
    leaf4 = LeafNode("img", "", {"src": "cat.jpg"})

    print(leaf4.to_html())

    parent_node = ParentNode("p", [leaf1, leaf2, leaf3])
    inner_parent = ParentNode("div", [leaf1, leaf2])
    outer_parent = ParentNode("p", [inner_parent, leaf3])
    print(parent_node.to_html())
    print(outer_parent.to_html())

def older_main():
    
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    print(split_nodes_delimiter([node], "`", TextType.CODE))

    meme_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(meme_text))

    dong_text = "This is an illegal link [to boot dev](https://www.boot.dev) and [to jewtube](https://www.youtube.com)"
    print(extract_markdown_links(dong_text))

    sample_text = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
    print(split_nodes_image([sample_text]))


    delim_bold_italic = TextNode("**bold** and *italic*", TextType.TEXT)
    
    meme = split_nodes_delimiter([delim_bold_italic], "**", TextType.BOLD)
    print(meme)
    meme = split_nodes_delimiter(meme, "*", TextType.ITALIC)
    print(meme)

    text = "This is *text* with an **italic** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    
    print(text_to_textnodes(text))

def text_main():
    
    textblock = """ # This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item
    """

    print(markdown_to_blocks(textblock))
    print("Below is a new test: \n\n")

    test_markdown = """# Main Heading # Because fuck you

This is a regular paragraph with *italic* and **bold** text.

## Second Level Heading

* First unordered item
* Second unordered item
* Third unordered item

1. First ordered item
2. Second ordered item
3. Third ordered item

> This is a blockquote
> with multiple lines
> and some *italic* text

```python
def sample_code():
	print("Hello World!")
```
"""

    blocks = markdown_to_blocks(test_markdown)
    for block in blocks:
        print("BLOCK:")
        print(block)
        print("END BLOCK")
        print()

    print("Below is the markdown_to_html_node test: \n\n\n")

    markdown_to_html_node(test_markdown)

    print("Below is the extract title test: \n\n\n")

    extract_title(test_markdown)

def lmao_main():
    
    item1 = LeafNode("li", "First item")
    item2 = LeafNode("li", "Second item", props={"class": "special"})

    ul = ParentNode("ul", children=[item1, item2], props={"class": "menu"})

    print(ul.to_html())

    markdown = """# Main Title

This is a **bold** paragraph with *italics*

* List item 1
* List item 2

```
code
```"""

    markup = """- **Bolded** List Item 1
- Bolded **List** Item 2
- Bolded List Item 3"""


    meow = markdown_to_html_node(markup)
    print(meow.to_html())
        
def main():
    
    nums = [12_345, 618_222, 58_832_221, 2_180_831_475, 8_663_863_102]

    average = 0
    if not nums:
        return None
    for num in nums:
        average += num
        average = average / len(nums)
    print(average)    
    return average


if __name__ == "__main__":
    main()
