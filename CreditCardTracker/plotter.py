import matplotlib.pyplot as plt
import numpy as np

def pieChartMonthYear(month_str, year_str, expenses_dict):
    expenses_categorized = np.array(list(expenses_dict.values()))
    plot_labels = []
    for i, category in enumerate(expenses_dict.keys()):
        plot_labels.append(f"{category}: ${expenses_categorized[i]:.2f}")

    plt.title(
        f"{month_str} {year_str} (Total Charges = ${sum(expenses_categorized):.2f})")
    plt.pie(expenses_categorized)
    plt.legend(plot_labels)
    plt.tight_layout()
    return

# Bar chart of expenses per month in a specified category
def plotCategoryYearInReview(year_str, expenses_dict_list, category_key, months_td_ordered):
    category_charges = []
    for month_indx, month_str in enumerate(months_td_ordered):
        expenses_dict = expenses_dict_list[month_indx]
        category_charges.append(expenses_dict[category_key])

    plt.title(f"{year_str} Year-in-review plot for {category_key}")
    plt.bar(range(len(months_td_ordered)), category_charges, align='center')
    plt.ylabel("Expense ($)")
    plt.xlabel("Month")
    plt.xticks(range(len(months_td_ordered)), months_td_ordered)
    plt.grid()
    return

# 12 pie charts for every month in the year
def plotYearInReviewPie(year_str, expenses_dict_list, months_td_ordered):
    nrows = 3
    ncols = 4
    plt.rcParams['figure.figsize'] = [18, 8]
    plt.subplots(nrows, ncols)
    for month_indx, month_str in enumerate(months_td_ordered):
        plt.subplot(nrows, ncols, month_indx+1)
        pieChartMonthYear(month_str, year_str, expenses_dict_list[month_indx])
    plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]
    return
