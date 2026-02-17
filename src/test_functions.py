from platform import node
import unittest

from textnode import *
from functions import *

class TestFunctions(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("This is some **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [TextNode("This is some text without delimiter", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, old_nodes)
    
    def test_split_nodes_delimiter2(self):
        old_nodes = [TextNode("Was zur Hölle ist eigentlich _italic_? Kursiv oder was)", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("Was zur Hölle ist eigentlich ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("? Kursiv oder was)", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches) 
        
    def test_extract_markdown_images2(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://www.example.com)")
        self.assertListEqual([("link", "https://www.example.com")], matches)
        
    def test_extract_markdown_links2(self):
        matches = extract_markdown_links("This is text with a [link](https://www.example.com) and another [link2](https://www.example2.com)")
        self.assertListEqual([("link", "https://www.example.com"), ("link2", "https://www.example2.com")], matches)   
    
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
        
    def test_split_images_no_images(self):
        node = TextNode("This is text without images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_split_mulit_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
    
    def test_split_links(self):
        node = TextNode("This is text with a [link](https://www.example.com) and another [second link](https://www.example2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.example2.com"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links_no_links(self):
        node = TextNode("This is text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_mulit_links(self):
        node = TextNode("This is text with a [link](https://www.example.com) and another [second link](https://www.example2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.example2.com"
                ),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        text = "This is some **bold** text with a [link](https://www.example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        text_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(expected_nodes, text_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_with_many_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
- Another list item

Here some code:
```
def hello_world():
    print("Hello, world!")
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items\n- Another list item",
                "Here some code:\n```\ndef hello_world():\n    print(\"Hello, world!\")\n```",
            ],
        )
        
    def test_blocl_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. List item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
    def test_extract_title(self):
        md = """# This is the title
This is some text in a paragraph.
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")
        
    def test_extract_title_no_title(self):
        md = """This is some text in a paragraph without a title"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("No title found in markdown" in str(context.exception))
        
    def test_extract_title_multiple_titles(self):
        md = """# This is the title
        ## This is a subtitle
        # This is another title
        """
        title = extract_title(md)
        self.assertEqual(title, "This is the title")    