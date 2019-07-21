from parser import *
from code_generator import *

if __name__ == '__main__':

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    
    # default values
    input_file = "input.txt"
    output_file = "output.txt"

    # parse command line arguments
    parser = ArgumentParser(
        description="translate functional code to MaMa language",
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-i", "--input", type=str, help="path to a file containing functional language", default=input_file)
    parser.add_argument("-o", "--output", type=str, help="path to output file", default=output_file)
    args = parser.parse_args()

    # usage: main.py [-h] [-i INPUT] [-o OUTPUT]
    #print(args.input)
    #print(args.output)

    # own examples
    '''
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

    # from lecture slides
    print(parse_tree("let rec fac = fun x -> if x <= 1 then 1 else x * fac (x-1) in fac 7")) # 102
    print()

    # TODO: for let f, first "in" is chosen (a in b)
    # print(parse_tree("let c = 5 in let f = fun a -> let b = a * a in b + c in f c")) # 114
    # print()
    
    print(parse_tree("let a = 19 in let b = a * a in a + b")) # 131
    print()

    print(parse_tree("let a = 17 in let f = fun b -> a + b in f 42")) # 140
    print()

    print(parse_tree("let rec f = fun x y -> if y <= 1 then x else f ( x * y ) ( y - 1 ) in f 1")) # 159
    print()
    '''

    ##examples handled by code generation
    #result = parse_tree("let a = 19 in let b = 17 * a in a + b") # 131
    #parse_syntaxTree(result)
    #result = parse_tree("if 1 then 3 else 4")
    #parse_syntaxTree(result)
    #result = parse_tree("let a = 17 in let f = fun b -> a + b in f (39 + 2)")
    #parse_syntaxTree(result)
    result = parse_tree("let a = 17 in let f = fun b -> a + b in f 42") # 140
    parse_syntaxTree(result)