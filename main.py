from parser import *

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
    print(args.input)
    print(args.output)

    # do actual work
    print(parse_tree("let a = 17 in let f = fun b -> a + b in f 42"))
    print()
    print(parse_tree("if a then 3 else 4"))