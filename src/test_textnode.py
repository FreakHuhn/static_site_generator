import unittest

from textnode import TextNode, TextType


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

        


if __name__ == "__main__":
    unittest.main()