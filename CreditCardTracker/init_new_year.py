# run this script whenever you want to initialize a new year

import os
from argparse import ArgumentParser

parser = ArgumentParser(prog="Credit Card Statement Tracker")

parser.add_argument('-y', '--year')

args = parser.parse_args()

year_str = args.year

# Initialize new year folders
for dir in ["Statements", "StatementsToProcess", "Plots", "YearInReview"]:
    if year_str not in os.listdir(dir):
        os.mkdir(f"{dir}/{year_str}")

print("-- Now, you can start adding monthly credit card transactions ({month}.csv) to the Statements/ folder...")