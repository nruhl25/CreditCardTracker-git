import os

# Initialize run directory before running code for the first time

os.system("touch categories.txt")

listdir = os.listdir()
for dir in ["VendorIDs", "YearInReview", "StatementsToProcess", "Plots", "Statements"]:
    if dir not in listdir:
        os.system(f"mkdir {dir}")