from tree_nodes import *
from parse import *
import numpy as np

def parse_brack(expr):
    if(parse("({e})", expr) is None):
        return None

    expr = expr[1:-1]
    expr = expr.split()

    counter = 1

    for word in expr:
        if word[0] == "(":
            counter += 1
        if word[-1] == ")":
            counter -= 1

        if not counter:
            return None

    x = dict()
    x['e'] = " ".join(expr)

    return x

def parse_let_rec(expr):

    expr = expr.split()
    if (len(expr) < 2 or expr[0] != "let" or expr[1] != "rec"):
        return None

    expr = expr[2:]
    counter = 1
    ind = -1

    for i in range(len(expr)):
        if (expr[i] == "let"):
            counter += 1
        elif (expr[i] == "in"):
            counter -= 1

            if(counter == 0):
                ind = i
                break

    if (ind == -1):
        return None
    
    x = dict()
    x['defs'] = " ".join(expr[:ind])
    x['e0'] = " ".join(expr[ind+1:])

    return x

def parse_and(defs):
    defs = defs.split()

    collect = []
    last = 0

    counter = 0
    for i in range(len(defs)):

        if(not counter and defs[i] == "and"):
            collect.append(defs[last:i])
            last = i+1
            continue

        if(defs[i] == "let"):
            counter += 1
            continue

        if(defs[i] == "in"):
            counter -= 1
            continue

    collect.append(defs[last:])

    defs = []

    for part in collect:
        defs.append(" ".join(part))

    return defs

def mk_rec(x, depth, dictio):
    defs = parse_and(x['defs'])

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

def parse_let(expr):

    expr = expr.split()
    if (len(expr) == 0 or expr[0] != "let"):
        return None

    counter = 0
    ind = -1

    for i in range(len(expr)):
        if (expr[i] == "let"):
            counter += 1
        elif (expr[i] == "in"):
            counter -= 1

            if(counter == 0):
                ind = i
                break

    if (ind == -1):
        return None

    tmp1 = expr[1:ind]
    e0 = expr[ind+1:]

    prs = parse("{x1} = {e1}", " ".join(tmp1))
    if(prs is None):
        return None
    
    x = dict()
    x['x1'] = prs['x1']
    x['e1'] = prs['e1']
    x['e0'] = " ".join(e0)

    return x

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

def split_expr(exprs):                      # TODO fix with own parsing approach
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

def check_brack(expr):
    count = 1

    for char in expr:
        if(char == '('):
            count += 1
        if(char == ')'):
            count -= 1

            if not count:
                return False

    return True

def mk_op2(x, depth, dictio, tag):
    e1 = parse_tree(x['e1'], depth+1, dictio)
    e2 = parse_tree(x['e2'], depth+1, dictio)
    return Other(tag, [e1, e2], depth)

def mk_op1(x, depth, dictio, tag):
    e = parse_tree(x['e'], depth+1, dictio)
    return Other(tag, [e], depth)

def is_known(expr, dictio, tag=""):
    if tag == "":
        return expr in dictio

    try: 
        return dictio[expr] == tag
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
    expr = ' '.join(expr.split())

    # (e)
    x = parse_brack(expr)
    if(x != None):
        return parse_tree(x['e'], depth, dictio)

    # let rec x1 = e1 and ... and xn = en in e0
    x = parse_let_rec(expr)
    if(x != None):
        return mk_rec(x, depth, dictio)

    # let x1 = e1 in e0
    x = parse_let(expr)
    if(x != None):
        return mk_let(x, depth, dictio)

    # fun x0 ... xk-1 -> e
    x = parse("fun {args} -> {e}", expr)
    if(x != None):
        return mk_fun(x, depth, dictio)
    
    # e' e0 ... ek−1
    x = expr.split(' ', 1)
    if(is_known(x[0], dictio, "fvar")):
        return mk_app(x, depth, dictio)

    # if e0 then e1 else e2
    x = parse("if {e0} then {e1} else {e2}", expr)
    if(x != None):
        return mk_if(x, depth, dictio)

    # e1 >= e2
    x = parse("{e1}>={e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "ge")

    # e1 > e2
    x = parse("{e1}>{e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "gt")

    # e1 <= e2
    x = parse("{e1}<={e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "le")

    # e1 < e2
    x = parse("{e1}<{e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "lt")

    # e1 == e2
    x = parse("{e1}=={e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "eq")

    # e1 != e2
    x = parse("{e1}!={e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "neq")

    # e1 + e2
    x = parse("{e1}+{e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "add")

    # e1 - e2
    x = parse("{e1}-{e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "sub")

    # e1 * e2
    x = parse("{e1}*{e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "mul")

    # e1 / e2
    x = parse("{e1}/{e2}", expr)
    if(x != None and check_brack(x['e2'])):
        return mk_op2(x, depth, dictio, "div")

    # +e
    x = parse("+{e}", expr)
    if(x != None):
        return mk_op1(x, depth, dictio, "uadd")

    # -e
    x = parse("-{e}", expr)
    if(x != None):
        return mk_op1(x, depth, dictio, "usub")

    # variable
    if(is_known(expr, dictio, "var")):
        return Variable("var", expr, depth)

    # argument
    if(is_known(expr, dictio, "arg")):
        return Variable("arg", expr, depth)

    # basic value
    if(is_int(expr)):
        return BasicValue("basic", int(expr), depth)

    # default case
    raise Exception('"{}" is not a valid expression.'.format(expr))
    # return Variable("dummy", expr, depth)