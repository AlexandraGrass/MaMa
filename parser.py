from tree_nodes import *
from parse import *
import numpy as np
import re

def mk_rec(x, depth, dictio):
    defs = x['defs'].split('and')

    new_dict = dictio.copy()

    children = []
    for defi in defs:
        y = parse("{x1} = fun {e1}", defi)
        if(y == None):
            raise Exception('"{}" is not a valid assignment in let rec.'.format(defi))

        new_dict[y['x1']] = "fvar"

    for defi in defs:
        y = parse("{x1} = {e1}", defi)

        x1 = Variable("fvar", y['x1'], depth+2)
        e1 = parse_tree(y['e1'], depth+2, new_dict)

        children.append(Other("asgn", [x1, e1], depth+1))

    e0 = parse_tree(x['e0'], depth+1, new_dict)
    children.append(e0)

    return Other("rec", children, depth)

def mk_let(x, depth, dictio):
    tag = "fvar" if x['e1'].split(' ', 1)[0] == "fun" else "var"

    new_dict = dictio.copy()

    x1 = Variable(tag, x['x1'], depth+2)
    new_dict[x['x1']] = tag

    e1 = parse_tree(x['e1'], depth+2, new_dict)

    asgn = Other("asgn", [x1, e1], depth+1)
    e0 = parse_tree(x['e0'], depth+1, new_dict)

    return Other("let", [asgn, e0], depth)

def mk_fun(x, depth, dictio):
    args = x['args'].split()

    new_dict = dictio.copy()
    
    children = []
    for arg in args:
        children.append(Variable("arg", arg, depth+1))
        new_dict[arg] = "arg"

    e = parse_tree(x['e'], depth+1, new_dict)
    children.append(e)

    return Other("fun", children, depth)

def split_expr(exprs):
    x = parse("({e1}) {e2}", exprs)
    if(x != None):
        tmp = [x['e1']]
        tmp.extend(split_expr(x['e2']))
        return tmp

    x = parse("({e})", exprs)
    if(x != None):
        return [x['e']]

    x = exprs.split(' ', 1)

    if len(x) == 1:
        return [x[0]]

    else:
        tmp = [x[0]]
        tmp.extend(split_expr(x[1]))
        return tmp

def mk_app(x, depth, dictio):
    children = [Variable("fvar", x[0], depth+1)]

    for expr in split_expr(x[1]):
        children.append(parse_tree(expr, depth+1, dictio))

    return Other("app", children, depth)

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

def is_known(expr, dictio):
    return expr in dictio

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

def is_fun(expr, dictio):
    try: 
        return dictio[expr] == "fvar"
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
    x = parse("let rec {defs} in {e0}", expr)
    if(x != None):
        return mk_rec(x, depth, dictio)

    # let x1 = e1 in e0
    x = parse("let {x1} = {e1} in {e0}", expr)
    if(x != None):
        return mk_let(x, depth, dictio)

    # fun x0 ... xk-1 -> e
    x = parse("fun {args} -> {e}", expr)
    if(x != None):
        return mk_fun(x, depth, dictio)
    
    # e' e0 ... ek−1
    x = expr.split(' ', 1)
    if(is_fun(x[0], dictio)):
        return mk_app(x, depth, dictio)

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