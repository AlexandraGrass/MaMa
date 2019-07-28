from parser import parse_tree
from code_generator import parse_syntaxTree

# own examples
print(parse_tree("let a = 17 in let f = fun b -> a + b in f (39 + 2)"))
print()
print(parse_tree("if 1 then 3 else 4"))
print()
print(parse_tree("let x3 = 4 in     +     x3    "))
print()
print(parse_tree("((34))"))
print()
print(parse_tree("3 / 4"))
print()
print(parse_tree("let rec f = fun x y -> if y <= 1 then x else f ( x * y ) ( y - 1 ) in f 1"))
print()
print(parse_tree("let y_x = 4 in y_x"))
print()

# examples handled by code generation
result = parse_tree("let a = 19 in let b = a * a in a + b") # 131
parse_syntaxTree(result)
print()
result = parse_tree("if 1 then 3 else 4")
parse_syntaxTree(result)
print()
result = parse_tree("let a = 17 in let f = fun b -> a + b in f (39 + 2)")
parse_syntaxTree(result)
print()
result = parse_tree("let a = 17 in let f = fun b -> a + b in f 42") # 140
parse_syntaxTree(result)
print()
result = parse_tree("let rec f = fun x y -> if y <= 1 then 5 else f ( x * y ) ( y - 1 ) in f 1")
parse_syntaxTree(result)
print()
result = parse_tree("let x3 = 4 in     +     x3    ")
parse_syntaxTree(result)

# needs work
'''
result = parse_tree("let f = fun x y -> let a = 5 in let b = x + 2*y in b + a*x in f 0 1")
parse_syntaxTree(result)
result = parse_tree("if y > x then x else 7 + y * x")
parse_syntaxTree(result)
'''