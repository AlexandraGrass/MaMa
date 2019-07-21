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

def check_var(var):
    for char in var:
        if ord(char) < 48 or ord(char) > 57 and ord(char) < 65 or ord(char) > 91 and ord(char) < 97 or ord(char) > 122:
            if not char == '_':
                raise Exception('"{}" is not a valid variable name.'.format(var))

    try:
        int(var[0])
        raise Exception('"{}" is not a valid variable name.'.format(var))
    except ValueError:
        pass

    if var[0] == '_' or var[-1] == '_':
        raise Exception('"{}" is not a valid variable name.'.format(var))

class Variable(Node):
    
    def __init__(self, tag, var, depth=0):
        if(tag != "dummy"):
            check_var(var)

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