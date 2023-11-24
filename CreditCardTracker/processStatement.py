from global_vars import reload_category_keys
import numpy as np
import pandas as pd

from tools import checkIfInCategory, loadVendorID_dict

# This function calculates an expenses_dict for the month/year specified
# expenses_dict = {CATEGORY: MONTHLY EXPENSE (float, $)} [derived from statements]
# It reads the "RawStatement"
def categorizeRawStatement(month_str, year_str):
    statement_fn = f"Statements/{year_str}/{month_str}.csv"
    # expenses_dict = {CATEGORY: MONTHLY EXPENSE (float, $)} [derived from Statements/]
    # vendorID_dict = {CATEGORY: LIST OF INCLUDED VENDORS (Vendors/)} [derived from recognized vendorIDs]

    category_keys = reload_category_keys()
    vendorID_dict = loadVendorID_dict(category_keys)

    # initalize expenses_dict
    expenses_dict = {}

    for category_key in category_keys:
        expenses_dict[category_key] = 0.0


    # Read in credit card statement for analysis
    df = pd.read_csv(statement_fn)
    vendorIDs_statement = np.array(df["Name"])
    charges_statement = -np.array(df["Amount"])
    auto_category_list = []

    # Categorize vendors/charges by their categories
    for i in range(len(vendorIDs_statement)):
        # At each vendor[i] Loop through the different categories within the budget
        count = 0
        for category_key in category_keys:
            if checkIfInCategory(vendorID_dict[category_key], vendorIDs_statement[i]):
                count += 1
                #TODO: don't include the credit card payment line
                expenses_dict[category_key] += charges_statement[i]
                auto_category_list.append(category_key)
        if count == 0:
            print(f"{vendorIDs_statement[i]} was not categorized")
        
    # Write ProcessedStatement excel file
    df.insert(len(df.columns), "Auto Category", auto_category_list)
    df.insert(len(df.columns), "Category Override", df.shape[0]*['None'])

    df.to_excel(f"StatementsToProcess/{year_str}/{month_str}.xlsx", index=False)

    print(f"---StatementsToProcess/{year_str}/{month_str}.xlsx has been written---")
    return expenses_dict
    
# This function reads the "StatementToProcess" instead of categorizing the Raw Statement
def readStatementToProcess(month_str, year_str, category_keys, all_vendorIDs):
    statement_fn = f"StatementsToProcess/{year_str}/{month_str}.xlsx"

    df = pd.read_excel(statement_fn)
    charges_statement = -np.array(df["Amount"])
    vendorIDs_statement = np.array(df["Name"])

    # Initialize expenses_dict and vendor_expense_dict
    expenses_dict = dict(zip(category_keys, np.zeros(len(category_keys))))
    vendor_expense_dict = dict(zip(all_vendorIDs, np.zeros(len(all_vendorIDs))))
    
    for i in range(len(vendorIDs_statement)):
        vendor_expense_dict[vendorIDs_statement[i]] += charges_statement[i]
        if df["Category Override"][i] == 'None':
            expenses_dict[df["Auto Category"][i]] += charges_statement[i]
        elif df["Category Override"][i] in category_keys:
            expenses_dict[df["Category Override"][i]] += charges_statement[i]
        else:
            print(f"Invalid entry in StatementsToProcess/{year_str}/{month_str}.xlsx: the category override {df['Auto Category'][i]} is not a valid category_key")

    return expenses_dict, vendor_expense_dict