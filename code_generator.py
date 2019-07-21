from tree_nodes import *

sd = 0
jumpId = 65
let_count = 0
rho = {}
localVarCount = 1

def parse_syntaxTree(tree):
    if(tree.tag == "if"):
        code_gen_for_if(tree.children)
    elif(tree.tag == "let"):
        code_gen_for_let(tree.children)
        print("slide " + str(let_count))

#code_generation for let
def code_gen_for_let(children):
    global let_count
    let_count+=1
    if(children[0].tag == "asgn"):
        code_gen_for_asgn(children[0].children)

    if(children[1].tag == "let"):
        code_gen_for_let(children[1].children)
    elif(children[1].tag == "app"):
        print(children[1].children)
    elif(children[1].tag == "add"):
        code_gen_for_op(children[1].children, "add")
    elif(children[1].tag == "mul"):
        code_gen_for_op(children[1].children, "mul")
    elif(children[1].tag == "sub"):
        code_gen_for_op(children[1].children, "sub")
    elif(children[1].tag == "div"):
        code_gen_for_op(children[1].children, "div")

#code_gen for assignment  
def code_gen_for_asgn(children):
    global rho, localVarCount
    if(children[0].tag == "var"):
        #print("Variable name: " + children[0].var + "added at" + str(localVarCount))
        rho[children[0].var] = localVarCount
        localVarCount += 1
        if(children[1].tag == "basic"):
            code_gen_for_basic_val(children[1].value)
        elif(children[1].tag == "mul"):
            code_gen_for_op(children[1].children, "mul")
    
    if(children[0].tag == "fvar"):
        print(children[0].var)
        if(children[1].tag == "basic"):
            print(children[1].value)
        elif(children[1].tag == "fun"):
            print(children[1].children)

#code_generation for basic
def code_gen_for_basic_val(value):
    global sd
    print(str(sd) + " loadc "+ str(value))
    sd+=1
    print(str(sd) +  " mkbasic")

#code_generation for var
def code_gen_for_var(var_name):
    global rho, sd
    value = rho[var_name]
    value = sd - value
    print(str(sd) + " pushloc " + str(value))
    sd+=1
    print(str(sd) + " getbasic")

#code_genation for binary operators
def code_gen_for_op(children, type):
    global sd
    if(children[0].tag == "var"):
        code_gen_for_var(children[0].var)
    elif(children[0].tag == "basic"):
        print(children[0].value)
    
    if (children[1].tag) == "var":
        code_gen_for_var(children[1].var)
    elif(children[1].tag == "basic"):
        print(children[1].value)

    print(str(sd) + " " + type)
    sd-=1
    print(str(sd) + " mkbasic")
        
#code_generation for if
def code_gen_for_if(children):
    global jumpId
    if_condition(children[0])
    print("jumpz " + chr(jumpId))
    jumpId+= 1
    if_then_expression(children[1])
    print("jump " + chr(jumpId))
    jumpId+= 1
    if_else_expression(children[2])

def if_condition(exp):
    if(exp.tag == "basic"):
        print("loadc " + str(exp.value))
    
def if_then_expression(exp):
    if(exp.tag == "basic"):
        print("loadc " + str(exp.value))

def if_else_expression(exp):
    if(exp.tag == "basic"):
        print("loadc " + str(exp.value))