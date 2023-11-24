# Import packages
from dash import register_page, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import os

from global_vars import reload_category_keys

register_page(__name__, path='/vendor_review')

category_keys = reload_category_keys()

years_to_date = os.listdir('StatementsToProcess')
years_to_date.remove(".DS_Store")
years_to_date_ints = [int(year) for year in years_to_date]
current_year = years_to_date[np.argmax(years_to_date_ints)]

# Read year in review files
df_dict = {}
for year in years_to_date:
    df_year = pd.read_excel(f'YearInReview/YearInReview2023.xlsx', sheet_name="VendorReview")
    df_dict[year] = df_year

# App layout
layout = html.Div([
    html.Div(children=f'Credit Card Expenses: Vendor Review'),
    html.Hr(), 
    dcc.Dropdown(options=years_to_date, value=current_year, id='year-dropdown'),
    dcc.Store(id='year_chosen'),
    html.Hr(),
    dash_table.DataTable(data=df_dict[current_year].to_dict('records'), page_size=10, id='category-data-table'),
    html.Hr(),
    html.Div(children=f'Which category do you want to see?'),
    dcc.RadioItems(options=category_keys, id='category_chosen'),
])