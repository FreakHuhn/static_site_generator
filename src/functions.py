import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            raise ValueError(f"Delimiter '{delimiter}' not found in text: '{node.text}'")
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    images = []
    for alt_text, url in matches:
        images.append(TextNode(alt_text, TextType.IMAGE, url))
    return images

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    links = []
    for anchor_text, url in matches:
        links.append(TextNode(anchor_text, TextType.LINK, url))
    return links    