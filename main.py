from parser import parse_tree
from code_generator import *    # TODO just import necessary method

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# default values
input_file = "input/test1.ml"
output_file = "output/test1.txt"

# parse command line arguments
parser = ArgumentParser(
    description="translate functional code to MaMa language",
    formatter_class=ArgumentDefaultsHelpFormatter
)
parser.add_argument("-i", "--input", type=str, help="path to a file containing functional language", default=input_file)
parser.add_argument("-o", "--output", type=str, help="path to output file", default=output_file)
args = parser.parse_args()

# usage: main.py [-h] [-i INPUT] [-o OUTPUT]

with open(args.input) as i_f:

    # read input and remove whitespace
    expr = i_f.read()
    expr = ' '.join(expr.split())

    # parse syntax tree
    tree = parse_tree(expr)

    # TODO generate code and print to file
    print(tree)
