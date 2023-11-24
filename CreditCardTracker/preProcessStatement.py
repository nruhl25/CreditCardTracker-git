import pandas as pd
import numpy as np
import os

from tools import checkIfInCategory, loadVendorID_dict
from global_vars import reload_category_keys

# Pre-process the statement, make sure that all charges are categorized
def preProcessStatement(month_str, year_str):
    print(f"----Pre-processing the 'Raw Statement' for {month_str} {year_str}----")

    statement_fn = f"Statements/{year_str}/{month_str}.csv"
    # Read in the statement
    df = pd.read_csv(statement_fn)
    raw_vendorIDs_statement = list(df["Name"])
    vendorIDs_statement = [raw_vendorID.strip() for raw_vendorID in raw_vendorIDs_statement]
    charges_statement = -np.array(df["Amount"])

    # {CATEGORY (str): LIST (str) OF INCLUDED VENDORS (VendorIDs/)}
    category_keys = reload_category_keys()
    vendorID_dict = loadVendorID_dict(category_keys)

    for i in range(len(vendorIDs_statement)):
        category_counter = 0  # becomes 1 if the vendorID has a match
        for key in category_keys:
            if checkIfInCategory(vendorID_dict[key], vendorIDs_statement[i]):
                category_counter += 1
            else:
                continue
        if category_counter == 0:
            print(
                f"---Vendor {vendorIDs_statement[i]} not recognized (${charges_statement[i]:.2f} charge)---")
            askUserToCategorize(
                vendorIDs_statement[i], charges_statement[i], category_keys)
            category_keys = reload_category_keys()
            vendorID_dict = loadVendorID_dict(category_keys)
        elif category_counter > 1:
            print(
                f"---WARNING: Vendor {vendorIDs_statement[i]} was recognized in {category_counter} different categories---")

    print(f"---{month_str} {year_str} statement has been pre-processed---")

    return

def askUserToCategorize(unknown_vendorID, unknown_vendorID_charge, category_keys):
    prompt = f"What category is {unknown_vendorID}? (${unknown_vendorID_charge} charge)?\n"
    for i in range(len(category_keys)):
        prompt = prompt + f"Press {i} for {category_keys[i]}\n"
    
    prompt = prompt + f"Enter 99 to make a new category\n"

    inp = int(input(prompt))

    if inp in range(0, len(category_keys)):
        os.system(f"echo '{unknown_vendorID}' >> VendorIDs/{category_keys[inp]}.txt")
    elif inp == 99:
        new_category = str(input("What category does this charge belong to (case-sensitive)?:\n"))
        os.system(f"echo '{new_category}' >> categories.txt")
        os.system(f"echo '{unknown_vendorID}' > VendorIDs/{new_category}.txt")
    else:
        raise RuntimeError("User input invalid")
    
    return 0
    
