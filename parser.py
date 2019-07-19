from tree_nodes import *
from parse import *
import numpy as np
import re

def mk_let(x, depth, dictio):
    x1 = Variable("var", x['x1'], depth+1)
    dictio[x['x1']] = "var"

    e1 = parse_tree(x['e1'], depth+1, dictio)
    e0 = parse_tree(x['e0'], depth+1, dictio)

    return Other("let", [x1, e1, e0], depth)

def mk_fun(x, depth, dictio):
    args = x['args'].split()
    
    children = []
    for arg in args:
        children.append(Variable("arg", arg, depth+1))
        dictio[arg] = "arg"

    e = parse_tree(x['e'], depth+1, dictio)
    children.append(e)

    return Other("fun", children, depth)

def mk_if(x, depth, dictio):
    e0 = parse_tree(x['e0'], depth+1, dictio)
    e1 = parse_tree(x['e1'], depth+1, dictio)
    e2 = parse_tree(x['e2'], depth+1, dictio)

    return Other("if", [e0, e1, e2], depth)

def mk_add(x, depth, dictio):
    e1 = parse_tree(x['e1'], depth+1, dictio)
    e2 = parse_tree(x['e2'], depth+1, dictio)
    return Other("add", [e1, e2], depth)

def mk_sub(x, depth, dictio):
    e1 = parse_tree(x['e1'], depth+1, dictio)
    e2 = parse_tree(x['e2'], depth+1, dictio)
    return Other("sub", [e1, e2], depth)

def mk_mul(x, depth, dictio):
    e1 = parse_tree(x['e1'], depth+1, dictio)
    e2 = parse_tree(x['e2'], depth+1, dictio)
    return Other("mul", [e1, e2], depth)

def mk_div(x, depth, dictio):
    e1 = parse_tree(x['e1'], depth+1, dictio)
    e2 = parse_tree(x['e2'], depth+1, dictio)
    return Other("div", [e1, e2], depth)

def mk_uadd(x, depth, dictio):
    e = parse_tree(x['e'], depth+1, dictio)
    return Other("uadd", [e], depth)

def mk_usub(x, depth, dictio):
    e = parse_tree(x['e'], depth+1, dictio)
    return Other("usub", [e], depth)

def is_var(expr, dictio):
    try: 
        return dictio[expr] == "var"
    except KeyError:
        return False

def is_arg(expr, dictio):
    try: 
        return dictio[expr] == "arg"
    except KeyError:
        return False

def is_int(expr):
    try: 
        int(expr)
        return True
    except ValueError:
        return False

def parse_tree(expr, depth=0, dictio={}):

    # remove unnecessary whitespace
    expr = re.sub(' +', ' ',expr).strip()

    # let rec x1 = e1 and ... and xn = en in e0
    # TODO

    # let x1 = e1 in e0
    x = parse("let {x1} = {e1} in {e0}", expr)
    if(x != None):
        return mk_let(x, depth, dictio)

    # fun x0 ... xk-1 -> e
    x = parse("fun {args} -> {e}", expr)
    if(x != None):
        return mk_fun(x, depth, dictio)
    
    # e' e0 ... ek−1
    # TODO

    # if e0 then e1 else e2
    x = parse("if {e0} then {e1} else {e2}", expr)
    if(x != None):
        return mk_if(x, depth, dictio)

    # e1 + e2
    x = parse("{e1}+{e2}", expr)
    if(x != None):
        return mk_add(x, depth, dictio)

    # e1 - e2
    x = parse("{e1}-{e2}", expr)
    if(x != None):
        return mk_sub(x, depth, dictio)

    # e1 * e2
    x = parse("{e1}*{e2}", expr)
    if(x != None):
        return mk_mul(x, depth, dictio)

    # e1 / e2
    x = parse("{e1}/{e2}", expr)
    if(x != None):
        return mk_div(x, depth, dictio)

    # +e
    x = parse("+{e}", expr)
    if(x != None):
        return mk_uadd(x, depth, dictio)

    # -e
    x = parse("-{e}", expr)
    if(x != None):
        return mk_usub(x, depth, dictio)

    # (e)
    x = parse("({e})", expr)
    if(x != None):
        return parse_tree(x['e'], depth, dictio)

    # variable
    if(is_var(expr, dictio)):
        return Variable("var", expr, depth)

    # argument
    if(is_arg(expr, dictio)):
        return Variable("arg", expr, depth)

    # basic value
    if(is_int(expr)):
        return BasicValue("basic", int(expr), depth)

    # default case
    # raise Exception('"{}" is not a valid expression.'.format(expr))
    return Variable("dummy", expr, depth)