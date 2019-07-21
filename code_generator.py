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
        print(str(sd) + " slide " + str(let_count))

#code_generation for let
def code_gen_for_let(children):
    global let_count
    let_count+=1
    if(children[0].tag == "asgn"):
        code_gen_for_asgn(children[0].children)

    if(children[1].tag == "let"):
        code_gen_for_let(children[1].children)
    elif(children[1].tag == "add"):
        code_gen_for_op(children[1].children, "add")
    elif(children[1].tag == "mul"):
        code_gen_for_op(children[1].children, "mul")
    elif(children[1].tag == "sub"):
        code_gen_for_op(children[1].children, "sub")
    elif(children[1].tag == "div"):
        code_gen_for_op(children[1].children, "div")
    elif(children[1].tag == "app"):
        code_gen_for_application(children[1].children)

#code_gen for assignment  
def code_gen_for_asgn(children):
    global rho, localVarCount
    if(children[0].tag == "var"):
        #print("Variable name: " + children[0].var + "added at" + str(localVarCount))
        rho[children[0].var] = ("L",localVarCount)
        localVarCount += 1
        if(children[1].tag == "basic"):
            code_gen_for_basic_val(children[1].value)
        elif(children[1].tag == "mul"):
            code_gen_for_op(children[1].children, "mul")
    
    if(children[0].tag == "fvar"):
        rho[children[0].var] = ("L",localVarCount)
        localVarCount+=1
        if(children[1].tag == "basic"):
            print(children[1].value)
        elif(children[1].tag == "fun"):
            code_gen_for_fun(children[1].children)
            
#code_generation for basic
def code_gen_for_basic_val(value):
    global sd
    print(str(sd) + " loadc "+ str(value))
    sd+=1
    print(str(sd) +  " mkbasic")

#code_generation for var
def code_gen_for_var(var_name, getbasic = True):
    global rho, sd
    value = rho[var_name][1]
    varType = rho[var_name][0]
    if varType == "L":
        value = sd - value
        print(str(sd) + " pushloc " + str(value))
    elif varType == "G":
        print(str(sd) + " pushglob " + str(value))
    sd+=1
    if (getbasic):
        print(str(sd) + " getbasic")

#code_genation for binary operators
def code_gen_for_op(children, type):
    global sd
    if(children[0].tag == "var"):
        code_gen_for_var(children[0].var)
    elif(children[0].tag == "basic"):
        code_gen_for_basic_val(children[0].value)
    
    if (children[1].tag == "var" or  children[1].tag == "arg"):
        code_gen_for_var(children[1].var)
    elif(children[1].tag == "basic"):
        code_gen_for_basic_val(children[1].value)

    print(str(sd) + " " + type)
    sd-=1
    print(str(sd) + " mkbasic")
        
#code_generation for if
def code_gen_for_if(children):
    global jumpId
    if(children[0].tag == "basic"):
        code_gen_for_basic_val(children[0].value)

    print("jumpz " + chr(jumpId))
    jumpId+= 1
    
    if(children[1].tag == "basic"):
        code_gen_for_basic_val(children[1].value)
    
    print("jump " + chr(jumpId))
    jumpId+= 1
    
    if(children[2].tag == "basic"):
        code_gen_for_basic_val(children[2].value)

#code_generation for function
def code_gen_for_fun(children):
    global sd, rho
    funArgVars = []
    for funArg in children:
        if (funArg.tag == "arg"):
            funArgVars.append(funArg.var)
        else:
            varsUsed = getVarsUsed() 
            freeVars = list(set(varsUsed) - set(funArgVars))
            #generate code for free-vars
            for var in freeVars:
                code_gen_for_var(var, False)
            print(str(sd) + " mkvec " + str(len(freeVars)))
            print(str(sd) + " mkfunval A")
            print(str(sd) + " jump B")
            oldSD = sd #new stack distance
            sd = 0
            oldRHO = rho
            rho = {}
            formalParamCount = 0
            globalFunVarCount = 0
            for var in funArgVars:
                rho[var] = ("L",formalParamCount)
                formalParamCount-=1
            for var in freeVars:
                rho[var] = ("G",globalFunVarCount)
                globalFunVarCount+=1
            print("A:")
            print (str(sd) + " targ " + str(len(funArgVars)))
            if (funArg.tag == "add"):
                code_gen_for_op(funArg.children, "add")
            
            print (str(sd) + " return " + str(len(funArgVars)))
            sd=oldSD
            rho = oldRHO
            print("B:")

#Return variables used inside a function inorder to determine the free variables
def getVarsUsed(): #TODO
    return ["a", "b"]

#code generation for function application
def code_gen_for_application(children):
    print(children)