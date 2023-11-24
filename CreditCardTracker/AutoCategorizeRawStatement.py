# First step in the process. Read and categorize the raw statement and make the StatementToProcess/ excel file

from argparse import ArgumentParser

from preProcessStatement import preProcessStatement
from processStatement import categorizeRawStatement
from global_vars import reload_category_keys

parser = ArgumentParser(prog="Credit Card Statement Tracker")

parser.add_argument('-m', '--month')
parser.add_argument('-y', '--year')

args = parser.parse_args()

# Pre-processing a statement is done in two steps for simiplicity

preProcessStatement(args.month, args.year)
expenses_dict = categorizeRawStatement(args.month, args.year)