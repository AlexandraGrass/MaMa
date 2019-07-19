from tree_nodes import *
from parse import *
import numpy as np
import re

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def mk_let(x, depth):
    x1 = Variable("var", x['x1'], depth+1)
    e1 = parse_tree(x['e1'], depth+1)
    e0 = parse_tree(x['e0'], depth+1)

    return Other("let", [x1, e1, e0], depth)

def mk_fun(x, depth):
    args = x['args'].split()
    
    children = []
    for arg in args:
        children.append(Variable("var", arg, depth+1))

    e = parse_tree(x['e'], depth+1)
    children.append(e)

    return Other("fun", children, depth)

def mk_if(x, depth):
    e0 = parse_tree(x['e0'], depth+1)
    e1 = parse_tree(x['e1'], depth+1)
    e2 = parse_tree(x['e2'], depth+1)

    return Other("if", [e0, e1, e2], depth)

def mk_add(x, depth):
    e1 = parse_tree(x['e1'], depth+1)
    e2 = parse_tree(x['e2'], depth+1)
    return Other("add", [e1, e2], depth)

def mk_sub(x, depth):
    e1 = parse_tree(x['e1'], depth+1)
    e2 = parse_tree(x['e2'], depth+1)
    return Other("sub", [e1, e2], depth)

def mk_mul(x, depth):
    e1 = parse_tree(x['e1'], depth+1)
    e2 = parse_tree(x['e2'], depth+1)
    return Other("mul", [e1, e2], depth)

def mk_div(x, depth):
    e1 = parse_tree(x['e1'], depth+1)
    e2 = parse_tree(x['e2'], depth+1)
    return Other("div", [e1, e2], depth)

def mk_uadd(x, depth):
    e = parse_tree(x['e'], depth+1)
    return Other("uadd", [e], depth)

def mk_usub(x, depth):
    e = parse_tree(x['e'], depth+1)
    return Other("usub", [e], depth)

def parse_tree(expr, depth=0):

    # remove unnecessary whitespace
    expr = re.sub(' +', ' ',expr).strip()

    # let rec x1 = e1 and ... and xn = en in e0
    # TODO

    # let x1 = e1 in e0
    x = parse("let {x1} = {e1} in {e0}", expr)
    if(x != None):
        return mk_let(x, depth)

    # fun x0 ... xk-1 -> e
    x = parse("fun {args} -> {e}", expr)
    if(x != None):
        return mk_fun(x, depth)

    # e' e0 ... ek−1
    # TODO

    # if e0 then e1 else e2
    x = parse("if {e0} then {e1} else {e2}", expr)
    if(x != None):
        return mk_if(x, depth)

    # e1 + e2
    x = parse("{e1}+{e2}", expr)
    if(x != None):
        return mk_add(x, depth)

    # e1 - e2
    x = parse("{e1}-{e2}", expr)
    if(x != None):
        return mk_sub(x, depth)

    # e1 * e2
    x = parse("{e1}*{e2}", expr)
    if(x != None):
        return mk_mul(x, depth)

    # e1 / e2
    x = parse("{e1}/{e2}", expr)
    if(x != None):
        return mk_div(x, depth)

    # +e
    x = parse("+{e}", expr)
    if(x != None):
        return mk_uadd(x, depth)

    # -e
    x = parse("-{e}", expr)
    if(x != None):
        return mk_usub(x, depth)

    # (e)
    x = parse("({e})", expr)
    if(x != None):
        return parse_tree(x['e'], depth)

    # basic value
    if(is_int(expr)):
        return BasicValue("basic", int(expr), depth)

    # variable (default case)
    return Variable("var", expr, depth)