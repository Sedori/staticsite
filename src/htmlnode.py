import re
from textnode import TextNode, TextType
from blocknode import markdown_to_blocks, block_to_block_type

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading" and block.startswith("# "):
            return block.lstrip("# ")
    raise Exception("No possible Title found")


def markdown_to_html_node(markdown):
    parent_node = ParentNode(tag="div", children=[])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        # determine the block type
        block_type = block_to_block_type(block)
        # match case
        match block_type:
            case "heading":
                level = 0
                for char in block:
                    if char == '#':
                        level += 1
                    else:
                        break
                tag = f"h{level}"
                text_nodes = text_to_textnodes(block.strip("# "))
                #print(text_nodes)
                
                child_nodes = []
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    child_nodes.append(html_node)

                node = ParentNode(tag=tag, children=child_nodes)
            
            case "code":
                text = block.strip("`").strip("\n").strip(" ")
                #print(text)
                code_node = LeafNode(tag="code", value=text)
                node = ParentNode(tag="pre", children=[code_node])

            case "block":
                lines = block.split("\n")
                cleaned_lines = [line.lstrip("> ") for line in lines]
                text = "\n".join(cleaned_lines)
                text_nodes = text_to_textnodes(text)

                child_nodes = []
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    child_nodes.append(html_node)

                node = ParentNode(tag="blockquote", children=child_nodes)
                #print("This is the case block output:", node)

            case "ulist":
                #print("This is the ulist block text:", block)
                list_items = []
                # break off the ulist into a python list
                lines = block.split("\n")
                for line in lines:
                    # strip and clean each line
                    cleaned_line = line[2:]
                    # transform it to a text_node
                    text_nodes = text_to_textnodes(cleaned_line)
                    # generate an empty list for use later
                    html_nodes = []
                    # text_to_textnodes output is a list so it has to be parsed like this
                    for text_node in text_nodes:
                        # gets transformed into an html_node
                        html_node = text_node_to_html_node(text_node)
                        # appended to the above empty list (html_nodes)
                        html_nodes.append(html_node)

                    li_node = ParentNode(tag="li", children=html_nodes)
                    list_items.append(li_node)

                node = ParentNode(tag="ul", children=list_items)
                #print("This is ulist's node:\n\n", node, "\n\n")

            case "olist":
                list_items = []

                lines = block.split("\n")
                for line in lines:
                    cleaned_line = line.lstrip("0123456789. ")
                    text_nodes = text_to_textnodes(cleaned_line)
                    html_nodes = []
                    for text_node in text_nodes:
                        html_node = text_node_to_html_node(text_node)
                        html_nodes.append(html_node)

                    li_node = ParentNode(tag="li", children=html_nodes)
                    list_items.append(li_node)

                node = ParentNode(tag="ol", children=list_items)
                #print("This is olist's node:\n\n", node, "\n\n")

            case "paragraph":
                text_nodes = text_to_textnodes(block)
                html_nodes = []
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    html_nodes.append(html_node)

                node = ParentNode(tag="p", children=html_nodes)
                #print("This is paragraph's node:\n\n", node, "\n\n")

        parent_node.children.append(node)
    #print(parent_node)
    return parent_node

        

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode("", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.text is None:
                raise ValueError("Images must have alt text for accessibility")
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Text Type does not exist currently!")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for each in old_nodes:
        if each.text_type != TextType.TEXT:
            new_node.append(each)
            continue

        split_nodes = []
        split_text = each.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(f"Missing closing delimiter: {delimiter}")
        for count, text in enumerate(split_text):
            if text == "":
                continue
            if count % 2 == 0:
                split_nodes.append(TextNode(text, TextType.TEXT))
            else:
                split_nodes.append(TextNode(text, text_type))
        
        new_node.extend(split_nodes)
            
    return new_node

def split_nodes_image(old_nodes):
    new_node = []
    for each in old_nodes:
        remaining_text = each.text
        extracted_images = extract_markdown_images(remaining_text)
        if not extracted_images:
            new_node.append(each)
        else:
            for alt_image in extracted_images:
                alt = alt_image[0]
                image = alt_image[1]
                sections = remaining_text.split(f"![{alt}]({image})", 1)
                if sections[0] != '':
                    new_node.append(TextNode(sections[0], TextType.TEXT))
                new_node.append(TextNode(alt, TextType.IMAGE, image))
                remaining_text = sections[1] if len(sections) > 1 else ''
            
            if remaining_text:
                new_node.append(TextNode(remaining_text, TextType.TEXT))

    return new_node
            

def split_nodes_link(old_nodes):
    new_node = []
    for each in old_nodes:
        remaining_text = each.text
        extracted_links = extract_markdown_links(remaining_text)
        if not extracted_links:
            new_node.append(each)
        else:
            for alt_link in extracted_links:
                alt = alt_link[0]
                link = alt_link[1]
                sections = remaining_text.split(f"[{alt}]({link})", 1)
                if sections[0] != '':
                    new_node.append(TextNode(sections[0], TextType.TEXT))
                new_node.append(TextNode(alt, TextType.LINK, link))
                remaining_text = sections[1] if len(sections) > 1 else ''

            if remaining_text:
                new_node.append(TextNode(remaining_text, TextType.TEXT))
    return new_node


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
            

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        props_list = [f'{key}="{value}"' for key, value in self.props.items()]

        return " " + " ".join(props_list)

    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

        if not isinstance(self.children, list):
            raise TypeError("Children must be provided as a list.")

    def to_html(self):
        if not self.tag:
            raise ValueError("No Tags!")
        if not self.children:
            raise ValueError("No Children!")
        html_result = f"<{self.tag}>"
        for child in self.children:
            html_result += child.to_html()

        html_result += f"</{self.tag}>"

        return html_result


