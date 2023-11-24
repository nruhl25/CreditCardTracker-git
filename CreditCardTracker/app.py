# This Dash App has different pages

# Import packages
import dash
from dash import Dash, html, dcc
import pandas as pd

# Initialize the app
app = Dash(__name__, use_pages=True, pages_folder='DashPages')

# App layout
app.layout = html.Div([
    html.Div("Visualize your Credit Card Statement with Dash!"),
    html.Div([
        dcc.Link(page['name']+" | ", href=page['path'])
        for page in dash.page_registry.values()
    ]),
    html.Hr(),

    # Contents of each page
    dash.page_container
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)