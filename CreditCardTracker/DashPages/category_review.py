# Import packages
from dash import register_page, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os
import numpy as np


register_page(__name__, path='/category_review')

years_to_date = os.listdir('StatementsToProcess')
years_to_date.remove(".DS_Store")
years_to_date_ints = [int(year) for year in years_to_date]
current_year = years_to_date[np.argmax(years_to_date_ints)]

# Read year in review files
df_dict = {}
for year in years_to_date:
    df_year = pd.read_excel(f'YearInReview/YearInReview2023.xlsx', sheet_name="CategoryReview")
    df_dict[year] = df_year

# App layout
layout = html.Div([
    html.Hr(),
    html.Div(children=f'Credit Card Expenses: Category Review'),
    dcc.Dropdown(options=years_to_date, value=current_year, id='year-dropdown'),
    dcc.Store(id='year_chosen'),
    html.Hr(),
    # replace Dropdown with category keys or create new radio items from year_chosen
    dcc.RadioItems(options=df_dict[current_year].columns[1:], id='category_chosen'),
    dash_table.DataTable(data=df_dict[current_year].to_dict('records'), page_size=10, id='year-data-table'),
    dcc.Graph(figure={}, id='year-in-review-graph')
])

# What year data table shows up
@callback(
        Output(component_id='year-data-table', component_property='data'),
        Input(component_id='year_chosen', component_property='data')
)
def update_review_table(year_chosen):
    return df_dict[year_chosen].to_dict('records')

# Interaction with category key radio buttons
@callback(
    Output(component_id='year-in-review-graph', component_property='figure'),
    [Input(component_id='category_chosen', component_property='value'),
    Input(component_id='year-dropdown', component_property='value')]
    )
def update_graph(category_chosen, year_chosen):
    fig = px.bar(df_dict[year_chosen], x='Month', y=category_chosen)
    return fig