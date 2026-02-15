import re
from textnode import *

# split_nodes_delimiter teilt TextNodes durch ein bestimmten Delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        count = node.text.count(delimiter)
        if count == 0:
            new_nodes.append(node)
            continue
        if count % 2 != 0:
            raise ValueError(
                f"Invalid Markdown: missing closing '{delimiter}' in text: '{node.text}'"
            )

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

# extract_markdown_images extrahiert alle Bilder aus einem Text und gibt eine Liste von (alt_text, url) zurück
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    images = []
    for alt_text, url in matches:
        images.append((alt_text, url))
    return images

# extract_markdown_links extrahiert alle Links aus einem Text und gibt eine Liste von (anchor_text, url) zurück
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    links = []
    for anchor_text, url in matches:
        links.append((anchor_text, url))
    return links

# split_nodes_image teilt TextNodes durch Bilder und erstellt neue TextNodes für die Bilder
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        text = node.text
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            if image_markdown in text:
                parts = text.split(image_markdown)
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
                text = parts[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

# split_nodes_link teilt TextNodes durch Links und erstellt neue TextNodes für die Links
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        text = node.text
        for anchor_text, url in links:
            link_markdown = f"[{anchor_text}]({url})"
            if link_markdown in text:
                parts = text.split(link_markdown)
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url=url))
                text = parts[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

# text_to_textnodes nimmt einen Text und gibt eine Liste von TextNodes zurück, die den Text in verschiedene Texttypen aufteilen
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

# markdown_to_blocks teilt einen Markdown-Text in Blöcke auf, die durch doppelte Zeilenumbrüche getrennt sind, und entfernt führende und folgende Leerzeichen
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

# block_to_block_type nimmt einen Block und gibt den entsprechenden BlockType zurück, basierend auf den Markdown-Syntax-Regeln
def block_to_block_type(block):
    if re.findall(r"^#{1,6} ", block):
        return BlockType.HEADING
    if re.findall(r"^> ", block):
        return BlockType.QUOTE
    if re.findall(r"^(\*|-|\+) ", block):
        return BlockType.UNORDERED_LIST
    if re.findall(r"^\d+\. ", block):
        return BlockType.ORDERED_LIST
    if re.findall(r"^```", block):
        return BlockType.CODE
    return BlockType.PARAGRAPH