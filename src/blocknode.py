from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "1"
    HEADING = "2"
    CODE = "3"
    QUOTE = "4"
    UNORDERED = "5"
    ORDERED = "6"


def markdown_to_blocks(markdown):
    new_markdown = []
    split_markdown = markdown.split("\n\n")
    for split_item in split_markdown:
        if split_item.strip() != "":
            new_markdown.append(split_item.strip())
        
    return new_markdown

def block_to_block_type(markdown_block): # can't be a list
    # header check
    if markdown_block.startswith("#"):
        for i in range(1, 7):
            if markdown_block.startswith("#" * i + " "):
                return f"heading"
    # code check
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return "code"
    # quote check
    if markdown_block.startswith("> "):
        split_markdown = markdown_block.split("\n")
        if all(lines.startswith("> ") for lines in split_markdown):
            return "block"
    # unordered list check
    if markdown_block.startswith(("* ", "- ")):
        split_markdown = markdown_block.split("\n")
        if all(lines.startswith(("* ", "- ")) for lines in split_markdown):
            return "ulist"
    # ordered list check
    if markdown_block.startswith("1."):
        split_markdown = markdown_block.split("\n")
        if all(line.startswith(f"{i}. ") for i, line in enumerate(split_markdown, start=1)):
            return "olist"
    # paragraph
    return "paragraph"

