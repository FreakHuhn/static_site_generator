

class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
  
    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

        
    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")
    
 
    def props_to_html(self):
        if not self.props:
            return ""
        
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        
        return props_str
    
class LeafNode(HtmlNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        self.tag = tag
        self.value = value
        self.props = props
    
    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, props={self.props})"

    
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        # Self-closing tags wie img
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"  
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        self.tag = tag
        self.children = children
        self.props = props 
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    

    