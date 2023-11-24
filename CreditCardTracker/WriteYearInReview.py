# Read the user-edited StatementToRead and make plot

# This should probably be a "YearInReview" script

from argparse import ArgumentParser
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys

from processStatement import readStatementToProcess
from global_vars import reload_category_keys, reload_vendorIDs
from tools import define_months_to_date_ordered, loadVendorID_dict
from plotter import pieChartMonthYear, plotCategoryYearInReview

parser = ArgumentParser(prog="Credit Card Statement Tracker")

parser.add_argument('-y', '--year')

args = parser.parse_args()

year = args.year

# year = '2023' # can use this instead of the user entered arg in debug mode

#### CALUCLATE EXPENSES_DICT FOR EACH MONTH THAT HAS PASSED THIS YEAR (args.year) ####

months_td_ordered = define_months_to_date_ordered(year)
category_keys     = reload_category_keys()
all_vendorIDs     = reload_vendorIDs(category_keys)

expenses_dict_list = [] # list of expenses_dict for each month
vendor_dict_list = [] # list for each month

for month_str in months_td_ordered:
    print(f"----Reading the 'Statement to process' for {month_str} {year}----")
    if f"{month_str}.xlsx" not in os.listdir(f"StatementsToProcess/{year}"):
        print(f"---> 'StatementsToProcess/{year}/{month_str}.xlsx' does not exist. User forgot to pre-process the statement with AutoCategorizeStatement.py. Exiting program...")
        sys.exit()
    else:
        expenses_dict, vendor_expenses_dict = readStatementToProcess(month_str, year, category_keys, all_vendorIDs)
        expenses_dict_list.append(expenses_dict)
        vendor_dict_list.append(vendor_expenses_dict)

##############################################################

# Add a toal column to the dictionary
category_keys_with_total = category_keys.copy()
category_keys_with_total.append("Total")

# Create the data frame for the CategoryReview page
for expenses_dict in expenses_dict_list:
    expenses_dict['Total'] = round(sum(expenses_dict.values()), 2)

data = np.zeros((len(months_td_ordered), len(category_keys_with_total)))
for i, expenses_dict in enumerate(expenses_dict_list):
    for j, expense in enumerate(expenses_dict.values()):
        data[i,j] = round(expense, 2)

df_category_review = pd.DataFrame(data, index=months_td_ordered, columns=category_keys_with_total)
df_category_review.index.name = "Month"

# Create the data frame for the vendor review
vendor_totals = np.zeros(len(all_vendorIDs))
for i, vendor_dict in enumerate(vendor_dict_list):
    vendor_totals += np.array(list(vendor_dict.values()))
sort_indx = np.flip(np.argsort(vendor_totals))

all_vendorIDs_array = np.array(all_vendorIDs, dtype=str)
sorted_vendorIDs = all_vendorIDs_array[sort_indx]
sorted_totals = vendor_totals[sort_indx]

data = np.zeros((len(months_td_ordered)+1, len(all_vendorIDs)))
for i, vendor_dict in enumerate(vendor_dict_list):
    unordered_vendor_expenses = np.array(list(vendor_dict.values()))
    ordered_vendor_expenses = unordered_vendor_expenses[sort_indx]
    for j, expense in enumerate(ordered_vendor_expenses):
        data[i,j] = round(expense, 2)
data[-1,:] = sorted_totals

months_td_ordered_with_total = months_td_ordered.copy()
months_td_ordered_with_total.append("Total")
df_vendor_review = pd.DataFrame(data, index=months_td_ordered_with_total, columns=sorted_vendorIDs)
df_vendor_review.index.name = "Month"

# Split up the vendor review into categories
recognized_vendorID_dict = loadVendorID_dict(category_keys)
# Sort Vendor review into sub-tables by category. Write the CategoryReview sheet
categorized_vendor_dict_list = np.empty(len(category_keys), dtype=dict)
for j, category in enumerate(category_keys):
    temp_dict = {}
    for vendor_i in sorted_vendorIDs: # sorted vendor_dict.keys()
        if vendor_i in recognized_vendorID_dict[category]:   
            temp_dict[vendor_i] = np.array(df_vendor_review[vendor_i])
    categorized_vendor_dict_list[j] = temp_dict
        # No error catching here... everything should only have one category at this point

# Write everything to excel

with pd.ExcelWriter(f"YearInReview/YearInReview{year}.xlsx") as writer:
    df_category_review.to_excel(writer, sheet_name="CategoryReview")
    df_vendor_review.to_excel(writer, sheet_name="VendorReview")

    for i, category in enumerate(category_keys):
        df_category = pd.DataFrame.from_dict(categorized_vendor_dict_list[i])
        df_category.index = months_td_ordered_with_total
        df_category.index.name = "Month"
        df_category.to_excel(writer, sheet_name=f"{category}Review")

print(f"----YearInReview/YearInReview{year}.xlsx has been written----")

#############################################################

for category in category_keys_with_total:
    plt.figure()
    plotCategoryYearInReview(year, expenses_dict_list, category, months_td_ordered)
    plt.savefig(f"Plots/{year}/{category}.png")

for i, month in enumerate(months_td_ordered):
    plt.figure()
    pieChartMonthYear(month, year, expenses_dict_list[i])
    plt.savefig(f"Plots/{year}/PieChart_{month}.png")

print(f"----Plots have been generated in Plots/{year}/----")
