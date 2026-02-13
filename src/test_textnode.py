from platform import node
import unittest

from textnode import *
from functions import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD.value)
        node2 = TextNode("This is a text node", TextType.BOLD.value)
        node3 = TextNode("This is a different text node", TextType.BOLD.value)
        node4 = TextNode("This is a text node", TextType.ITALIC.value)
        node5 = TextNode("This is a text node", TextType.BOLD.value, "https://www.example.com") 
        node6 = TextNode("This is a text node", TextType.IMAGE.value, "https://www.example.com") 
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertNotEqual(node, node6)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
        
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
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    
    def test_split_nodes_delimiter2(self):
        old_nodes = [TextNode("Was zur Hölle ist eigentlich _italic_? Kursiv oder was)", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("Was zur Hölle ist eigentlich ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("? Kursiv oder was)", TextType.TEXT)
        ]
    

if __name__ == "__main__":
    unittest.main()