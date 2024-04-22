import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Dash
from .utils import get_data
from flask import render_template_string
from flask import Flask, Blueprint, render_template
from src import app as flask_app
import flask
from flask_login import current_user

df = get_data()

style_header = {'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'}
style_data = {'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'}
style_table = {
    'height': '300px',
    'overflowX': 'auto',
    'overflowY': 'auto',
    'border': '1px solid white',
    'width' : "100%"
}
style_plot = {
        'height': '500px',  # Adjust the height as needed
        'flex': '1'     # Adjust the width as needed, 100% for full width
    }

intro = '''The app displays the data from transactions from Kroger transactions, and their related households and products. The data is useful in understanding consumer buying patterns.'''
file_guidelines = '''Please upload a **zip file containing 3 csvs**. The csvs should contain names i.e **products, households and transactions** for proper processing.'''
plot_comments = """We calculated the total spend by each household for the data to represent the consumer engagement. We performed linear regression with each factor to find out its effect on the consumer spend. We find that household size has the maximum effect on the consumer spend with an r-squared score of 0.88. This means that household size can be used to predict the consumer spend. However, these results are performed on the aggregated data, so their predictive power is very less."""
plot_table = """
| Factor                    | R-squared Value |
|--------------------------------|-----------------|
| Number of Children | 0.87              |
| Income Range       | 0.74              |
| Age Range          | 0.66              |
| Household Size     | 0.88              |
"""
ml_comments = """Random Forest was used to perform predictive modeling of the consumer spend. Age range, income range, number of children, household size and the store. Random forest was successfully able to predict the total spend of the households for the data within 10% of the value.

### Pre-processing:

Following cleaning steps were performed:

- Outlier removal
- Train/Test Split with 80% 20% split.
- Conversion of categorical columns to one hot encoded columns

 

### Processing:

Random Forest was used to perform the predictive modeling. The reason to use the random forest were explainability, fast training an inference times.

### Results

Following results were obtained:

Mean Absolute Percentage Error: 9.93%
RMSE Error: 1890.03
R2 Score: 0.91

This proves that using all the data, we can predict the total spend of the households within 10% accuracy.

### Feature Importance:

As seen in the plot, the ages 35-44 had the most affect on the prediction of the total spend. The second most important feature was having no children, followed by income range of 35K to 44K and then the store. Above factors had the most prominent effect on the outcome i.e. most predicting power."""


table = dash_table.DataTable(
    id='table-paging-with-graph',
    columns=[{"name": i, "id": i} for i in df.columns],
    page_size=20,
    page_action='custom',
    virtualization=True,
    style_header=style_header,
    style_data=style_data,
    style_table=style_table,
    style_cell={'textAlign': 'center', 'minWidth': '100px', 'width': '150px', 'maxWidth': '180px'},
)

hhd_dd = dcc.Dropdown(
    id='df-household',
    options=[{'label': x, 'value': x} for x in sorted(df['HSHD_NUM'].unique())],
    value=df['HSHD_NUM'].iloc[0],
    placeholder="Select a Household",
    style={'color': '#000'}
)

hhd_heading = html.Div(children='Select Household')

data_dd = dcc.Dropdown(
    id='df-data',
    options=[{'label': x, 'value': x} for x in ['8451_sample', 'my_data']],
    value='8451_sample',
    placeholder="Select a Data",
    style={'color': '#000'}
)


upload_button = dcc.Upload(
    id='upload-data',
    children=html.Button('Upload Data', className='btn btn-primary'),
    multiple=False,
    style= {"align" : "center", 'padding': 10,}
)

upload_status = html.Div(id='upload-status', style={'color': 'green', 'fontSize': '20px',})

children_plot = html.Iframe(src=r"assets\average_spend_per_children.html",
                                 style=style_plot)
income_plot = html.Iframe(src=r"assets\average_spend_per_income_range.html",
                                 style=style_plot)
hhd_plot = html.Iframe(src=r"assets\average_spend_per_household_size.html",
                                 style=style_plot)
store_plot = html.Iframe(src=r"assets\average_spend_per_store.html",
                                 style=style_plot)
age_plot = html.Iframe(src=r"assets\average_spend_per_age_range.html",
                                 style=style_plot)
features_plot = html.Iframe(src=r"assets\features.html",
                                 style=style_plot)


nav_bar = html.Div([
    html.H1(children="Dashboard", style={"textAlign" : "center"}),
    dcc.Markdown(intro, style={"textAlign" : "center"}),
    html.Hr()])

selection_row = html.Div([
    dbc.Col(html.Div([
        html.Label("Select Household"),
        hhd_dd,
        html.Br(),
        html.Label("Select Data"),
        data_dd,
        html.Br(),
        dcc.Markdown(file_guidelines),
        upload_button,
        html.Br(),
        upload_status,
    ]), width=6, style={'padding': 5}),  # Adjust width as needed

    dbc.Col(html.Div([
        table
    ]), width=6, style={'padding': 5})  # Adjust width as needed
], style={'display': 'flex'})

plot_heading = html.Div(children=(
    html.H1("Analysis of Factors", style={'textAlign' : "center"}),
    dcc.Markdown(plot_comments, style={'textAlign' : "center"}),
    dcc.Markdown(plot_table),
    html.Br()
))

plot_row_1 = html.Div(children=[children_plot, income_plot, age_plot], style={'display': 'flex'})
plot_row_2 = html.Div(children=[hhd_plot, store_plot], style={'display': 'flex'})

ml_heading = html.Div(children=(html.Br(), dcc.Markdown(ml_comments, style=style_plot), features_plot), style={'display': 'flex'})

layout = dbc.Container([
    dbc.Row([
        nav_bar
    ], justify='center'),
    dbc.Row([selection_row,
    ], justify='start'),

    dbc.Row(plot_heading, style={'textAlign' : "center"}),
    dbc.Row(plot_row_1),
    dbc.Row(plot_row_2),
    dbc.Row(html.Div([html.Br(), html.H1("Machine Learning Prediction")])),
    dbc.Row(ml_heading),
], fluid=True)
