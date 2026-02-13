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
