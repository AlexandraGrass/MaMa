class Node(object):
    
    def __init__(self, tag, depth=0):
        self.tag = tag
        self.depth = depth

    def __str__(self):
        return " " * self.depth + self.tag

class BasicValue(Node):
    
    def __init__(self, tag, value, depth=0):
        self.value = value
        super(BasicValue, self).__init__(tag, depth)

    def __str__(self):
        super_str = super(BasicValue, self).__str__()
        return super_str + ": " + str(self.value)

class Variable(Node):
    
    def __init__(self, tag, var, depth=0):
        self.var = var
        super(Variable, self).__init__(tag, depth)

    def __str__(self):
        super_str = super(Variable, self).__str__()
        return super_str + ": " + self.var

class Other(Node):
    
    def __init__(self, tag, children, depth=0):
        self.children = children
        super(Other, self).__init__(tag, depth)

    def __str__(self):
        super_str = super(Other, self).__str__()
        return super_str + ":\n" + '\n'.join(map(str, self.children))