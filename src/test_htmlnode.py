"""
Docstring for test_htmlnode

Create some tests for the HTMLNode class (at least 3). I used a new file called src/test_htmlnode.py. Create a few nodes and make sure the props_to_html method works as expected.
"""
import unittest
from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HtmlNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HtmlNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com" target="_blank"')

    def test_props_to_html_with_empty_props(self):
        node = HtmlNode(tag="span", props={})
        self.assertEqual(node.props_to_html(), "")
        
        
if __name__ == "__main__":    unittest.main()