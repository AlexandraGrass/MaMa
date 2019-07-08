class Node(object):
    
    def __init__(self, tag):
        self.tag = tag

class BasicValue(Node):
    
    def __init__(self, tag, value):
        self.value = value
        super(BasicValue, self).__init__(tag)

class Variable(Node):
    
    def __init__(self, tag, var):
        self.var = var
        super(Variable, self).__init__(tag)

class Other(Node):
    
    def __init__(self, tag, children):
        self.children = children
        super(Other, self).__init__(tag)