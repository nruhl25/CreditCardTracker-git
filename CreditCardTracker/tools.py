# Various utility function for the credit card statement processor
import os

from global_vars import months

# Function to check if there is a vendorString[i] that matches statementString
def checkIfInCategory(vendorString_list, statementString):
    for i in range(len(vendorString_list)):
        if vendorString_list[i] == statementString:
            return True
        else:
            continue
    return False


def define_months_to_date_ordered(year_str):
    months_csv = os.listdir(f'Statements/{year_str}')
    months_to_date = []
    months_td_ordered = []

    for fn in months_csv:
        if fn == ".DS_Store":
            continue
        indx = fn.rfind('.')
        months_to_date.append(fn[0:indx])

    for month_i in months:
        if month_i in months_to_date:
            months_td_ordered.append(month_i)

    return months_td_ordered

# Load the dictionary of recognized vendorID's

def loadVendorID_dict(category_keys):
    # create dict of category and vendor pairs
    # {CATEGORY (str): LIST (str) OF INCLUDED VENDORS (VendorIDs/)}
    vendorID_dict = {}
    
    for key in category_keys:
        f_key = open(f"VendorIDs/{key}.txt", "r")
        raw_vendorIDs_recognized = f_key.readlines()
        f_key.close()
        vendorID_dict[key] = [raw_vendorID_recognized.strip()
                              for raw_vendorID_recognized in raw_vendorIDs_recognized]
    return vendorID_dict