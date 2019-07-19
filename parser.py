from tree_nodes import *
from parse import *
import numpy as np

# TODO: Rho for vars & funs, several statements, conditions, var vs arg

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def parse_tree(code, depth=0):

    # let x1 = e1 in e0
    x = parse("let {x1} = {e1} in {e0}", code)
    if(x != None):
        x1 = Variable("var", x['x1'], depth+1)
        e1 = parse_tree(x['e1'], depth+1)
        e0 = parse_tree(x['e0'], depth+1)

        return Other("let", [x1, e1, e0], depth)

    # fun x0 ... xk-1 -> e
    x = parse("fun {args} -> {e}", code)
    if(x != None):
        args = x['args'].split()
        
        children = []
        for arg in args:
            children.append(Variable("var", arg, depth+1))

        e = parse_tree(x['e'], depth+1)
        children.append(e)

        return Other("fun", children, depth)

    # if e0 then e1 else e2
    x = parse("if {e0} then {e1} else {e2}", code)
    if(x != None):
        e0 = parse_tree(x['e0'], depth+1)
        e1 = parse_tree(x['e1'], depth+1)
        e2 = parse_tree(x['e2'], depth+1)

        return Other("if", [e0, e1, e2], depth)

    # basic value
    if(is_int(code)):
        return BasicValue("basic", int(code), depth)

    # variable (default case)
    return Variable("var", code, depth)