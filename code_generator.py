from tree_nodes import *

sd = 0 #stack distance
jumpId = 65 #Labels to jump to
let_count = 0 #Count lets to slide at the end
rho = {} #Address space
localVarCount = 1 #local variable count
varsUsedInFun = [] #to find all variables used in the function def inorder to find the free variables
otherType = ["add", "sub", "mul", "div", "if", "asgn", "let", "fun", "if","app"] #all tags for type 'Other'
opType = ["add", "sub", "mul", "div"] #binary operators
op2 = ["le", "lt", "ge", "gt", "eq"] #Comparision operators
localAssignmentCount = 0

###parsing of the code called from main
def parse_syntaxTree(tree): #Assume the program starts with only let, if and let_rec
    if(tree.tag == "if"):
        code_gen_for_if(tree.children)
    elif(tree.tag == "let"):
        code_gen_for_let(tree.children)
        print(str(sd) + " slide " + str(let_count))
    elif(tree.tag == "rec"):
        code_gen_for_rec(tree.children)

###code_generation generic call
def code_generation(child, basic = True, var=True):
    if(child.tag == "asgn"):
        code_gen_for_asgn(child.children)

    if(child.tag == "let"):
        code_gen_for_let(child.children)
    
    if(child.tag in opType):
        code_gen_for_op(child.children, child.tag)

    if(child.tag == "app"):
        code_gen_for_application(child.children)

    if(child.tag == "uadd" or child.tag == "usub"):
        code_gen_for_uop(child.children, child.tag)

    if(child.tag == "var" or child.tag == "arg" or child.tag == "fvar"):
        code_gen_for_var(child.var, var)
    
    if(child.tag == "basic"):
        code_gen_for_basic_val(child.value, basic)
   
    if(child.tag == "if"): 
        code_gen_for_if(child.children)

    if(child.tag == "fun"):
        code_gen_for_fun(child.children)

    if(child.tag in op2):
        code_gen_for_op(child.children, child.tag)

###code_generation for let
def code_gen_for_let(children):
    global let_count
    let_count+=1 #increment every time a let statement is encountered
    code_generation(children[0])
    code_generation(children[1])

###code_generation for unary operators
def code_gen_for_uop(children, type):
    code_generation(children[0])
    print(str(sd) + " " +type)
    print(str(sd) + " mkbasic")

###code_gen for assignment  
def code_gen_for_asgn(children):
    global rho, localVarCount
    #first child of assignment can be a var or an fvar. If its a var the second child will be a basic value, an if or a binary operator. If its an fvar, the second child is a function
    if(children[0].tag == "var"):
        rho[children[0].var] = ("L",localVarCount)
        localVarCount += 1
        code_generation(children[1])
    
    if(children[0].tag == "fvar"):
        rho[children[0].var] = ("L",localVarCount)
        localVarCount+=1
        code_generation(children[1])
            
###code_generation for basic value 
def code_gen_for_basic_val(value, makebasic = True):
    global sd
    print(str(sd) + " loadc "+ str(value))
    sd+=1
    if (makebasic == True): #codeV
        print(str(sd) +  " mkbasic")

###code_generation for var
def code_gen_for_var(var_name, getbasic = True):
    global rho, sd
    varType = rho[var_name][0]
    value = rho[var_name][1]
    #check if the variable is local or global
    if varType == "L":  
        value = sd - value
        print(str(sd) + " pushloc " + str(value))
    elif varType == "G":
        print(str(sd) + " pushglob " + str(value))
    sd+=1
    if (getbasic):  #codeV
        print(str(sd) + " getbasic")

###code_generation for binary operators
def code_gen_for_op(children, type): #The children of operators can be var arg or basic
    global sd
    code_generation(children[0], False, True)
    code_generation(children[1], False, True)
    print(str(sd) + " " + type)
    sd-=1
    if (type in opType):
        print(str(sd) + " mkbasic") 
        
###code_generation for if
def code_gen_for_if(children): 
    global jumpId
    code_generation(children[0], False, True)
    elseJumpId = jumpId
    print(str(sd) + " jumpz " + chr(elseJumpId))
    jumpId+= 1
    
    #then part of if can be basic, var or arg type
    code_generation(children[1], True, False)
    
    postElseJumpId = jumpId
    print(str(sd) + " jump " + chr(postElseJumpId))
    print(chr(elseJumpId) + ":")
    jumpId+= 1

    #else part of if can be either basic or application type
    code_generation(children[2])
    print(chr(postElseJumpId) + ":")
    
###code_generation for function
def code_gen_for_fun(children):
    global sd, rho, jumpId
    funArgVars = [] #the formal parameters
    localFunNameLabel = jumpId #label for the function name to be created
    jumpId += 1
    localFunJumpLabel = jumpId #label for the jump after the function call
    jumpId += 1
    for funArg in children: #there could be 1-n parameters for the function
        if (funArg.tag == "arg"):   
            funArgVars.append(funArg.var)
        else:               #the actual execution of the function
            varsUsed = getVarsUsed(children)   #all variables used inside the function definition
            freeVars = list(set(varsUsed) - set(funArgVars))    #variables that are not formal parameters
            varsUsedInFun = []  #reset the global variable
            
            for var in freeVars:    #first generate code for free-vars
                code_gen_for_var(var, False)
            print(str(sd) + " mkvec " + str(len(freeVars)))
            print(str(sd) + " mkfunval " + chr(localFunNameLabel))
            print(str(sd) + " jump " + chr(localFunJumpLabel))
            
            oldSD = sd #new stack distance and address space in the function definiton
            sd = 0
            oldRHO = rho
            rho = {}
            formalParamCount = 0
            globalFunVarCount = 0
            
            for var in funArgVars:  #define the address space of the local and formal parameters
                rho[var] = ("L",formalParamCount)
                formalParamCount-=1
            for var in freeVars:
                rho[var] = ("G",globalFunVarCount)
                globalFunVarCount+=1

            print(chr(localFunNameLabel) + ":") #start of the function definition code generation
            print (str(sd) + " targ " + str(len(funArgVars)))
            
            code_generation(funArg)
            
            print (str(sd) + " return " + str(len(funArgVars))) #end of the function definition code generation
            
            sd=oldSD    #reset the sd and the address space
            rho = oldRHO
            print(chr(localFunJumpLabel) + ":")

#Return variables used inside a function inorder to determine the free variables
def getVarsUsed(children):
    global varsUsedInFun
    for i in children:
        if (i.tag == "var" or i.tag == "fvar" or i.tag == "arg"):
            if(not i.var in varsUsedInFun):
                varsUsedInFun.append(i.var)
        elif (i.tag in otherType): 
            getVarsUsed(i.children)
    return varsUsedInFun

###code generation for function application
def code_gen_for_application(children):
    global sd, jumpId
    preAppSD = sd
    localMarkVar = jumpId #label for the jump after the function application
    jumpId+=1
    print(str(sd) + " mark " + chr(localMarkVar))
    sd=sd+3 #three org cells loaded
    for i in range((len(children)-1),-1, -1): #the children are read in reverse order and are either basic, binary operator or a fvar
        code_generation(children[i], True, False)
    print(str(sd) + " apply")
    print(chr(localMarkVar) + ":")
    sd = preAppSD + 1 

###code generation for rec
def code_gen_for_rec(children):
    global sd
    n = allocateLocalVars(children) #find no of local variables to be allocated
    print(str(sd) + " alloc " + str(n))
    sd+=n
    code_generation(children[0])
    print(str(sd) + " rewrite " + str(n))
    sd-=1
    code_generation(children[1])
    print(str(sd) + " slide " + str(n))

#find the value of n for rec definitions
def allocateLocalVars(children):
    global localAssignmentCount
    for i in children:
        if (i.tag == "asgn"):
            localAssignmentCount+=1
        elif (i.tag == "var" or i.tag == "fvar" or i.tag == "basic" or i.tag == "arg"):
            pass
        else:
            allocateLocalVars(i.children)
    return localAssignmentCount

#Old code
#code_gen_for_op
'''if(children[0].tag == "var" or children[0].tag == "arg"): 
        code_gen_for_var(children[0].var)
    elif(children[0].tag == "basic"):
        code_gen_for_basic_val(children[0].value, False)
    
    if (children[1].tag == "var" or  children[1].tag == "arg"):
        code_gen_for_var(children[1].var)
    elif(children[1].tag == "basic"):
        code_gen_for_basic_val(children[1].value, False)'''

#code_gen_for_if
'''if(children[0].tag == "basic"): #the condition can be a basic type or a op2 type
        code_gen_for_basic_val(children[0].value, False)
    elif(children[0].tag in op2):
        code_gen_for_op(children[0].children, children[0].tag)'''
'''if(children[1].tag == "basic"): 
        code_gen_for_basic_val(children[1].value)
    elif(children[1].tag == "var" or children[1].tag == "arg"):
        code_gen_for_var(children[1].var, False)'''
'''if(children[2].tag == "basic"):
        code_gen_for_basic_val(children[2].value)
    elif (children[2].tag == "app"):
        code_gen_for_application(children[2].children)'''

#code_gen_for_function_application
'''if(children[i].tag == "basic"):
            code_gen_for_basic_val(children[i].value)
        elif(children[i].tag in opType):
            code_gen_for_op(children[i].children,children[i].tag)
        elif(children[i].tag == "fvar"):
            code_gen_for_var(children[i].var,False)'''
