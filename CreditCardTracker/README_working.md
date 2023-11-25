### Credit Card Tracker
#### Author: Nathaniel Ruhl


##### Usage of the Command-Line Interface:

###### Set-up requirements for running the code
1. Create a new folder which contains 9 python scripts:
-  \_\_init\_\_.py
- init_new_year.py
- global_vars.py
- tools.py
- plotter.py
- preProcessStatement.py
- processStatement.py
- AutoCategorizeRawStatement.py
- WriteYearInReview.py

    - DashPages/ folder and app.py are required for the Dash application

The executable files required in the program are
-  \_\_init\_\_.py
- init_new_year.py
- AutoCategorizeRawStatement.py
- WriteYearInReview.py

2. The first time running the program in an area, run the script \_\_init\_\_.py to make the required sub-directories
`python __init__.py`
3. Every time you want to start analyzing a new year, run the command
`python init_new_year.py -y {year}`

###### Pre-processing of a new credit card statement:
1. Download the .csv file for expenses from the first to last day of a month. Name this "{month}.csv" and put it in the folder "Statements/{year}/"
2. Remove the entry "THANK YOU" row from the .csv file. This is the credit card payment for the previous month (I may put in functionality to ignore this in the future, but it is not yet implemented)
3. From the "CreditCardTracker/" directory, run the pre-processing script from the command line:

`python AutoCategorizeStatement.py -m {month} -y {year}`

4. The program will ask the user to categorize any un-recognized vendors

5. An exel file "{month}.xlsx" will be written in the folder "StatementsToProcess/{year}/" which contains a copy of the credit card statement with a new column indicating the auto-categorization of the expense

6. Only run this command once per statement, unless you want to re-write the Statement-to-process file

###### Manually updating the "Statement to Process"
1. The "Statement to Process" allows the user to "over-write" the auto-categorization done by the program. In the column named "Category Over-ride", the user can replace "None" with the desired category (this category must be valid and appear in categories.txt)
2. You can also add rows to the excel file. For example, you can manually add Venmo charges to the bottom of the table, or you could split up a \$100 Costco charge into a row with \$50 of "Clothes_and_Furniture" and another row with \$50 of "Groceries"
3. If the auto-category override column entry is blank, the program will use the auto-category, otherwise it will use the over-ride

###### Writing the "Year in Review" excel file and generating summary plots
1. From the "CreditCardTracker/" directory, run the processing script from the command line:

`python WriteYearInReviw.py -y {year}`

2. This script processes all of the months that have happened in the {year} argument, writes the YearInReview{year}.xlsx file and writes a new set of plots in the Plots/ folder

###### Interactive Data Visualization with Dash
1. Run the Dash app to visualize YearInReview Data:
`python app.py`

###### Functionality to add to the program
- Make a GitHub repo for this project
- Figure out how I want to implement a monthly budget into the code
- Make sure it works if you wanted to split up cost from one store into different categories
- Functionality to handle a refund?
- Add the "VendorReview" page to my Dash App
- Can make a "Monthly Review" Page with the pie charts
- Make an excel sheet to track salary by year


