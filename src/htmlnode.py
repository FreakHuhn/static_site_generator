

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