import dash
from dash import html, dcc, dash_table, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache
from flask import Flask

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE], server=flask_app, )
cache = Cache(app.server, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': 'cache-directory'})

# Data loading and preprocessing
def load_and_combine_data():
    # Paths
    hhd_path = r"C:\Work\Courses\Intro to Cloud Computing\myflaskapp\data\8451_sample\400_households.parquet"
    pd_path = r"C:\Work\Courses\Intro to Cloud Computing\myflaskapp\data\8451_sample\400_products.parquet"
    tr_path = r"C:\Work\Courses\Intro to Cloud Computing\myflaskapp\data\8451_sample\400_transactions.parquet"
    
    hhd_df = pd.read_parquet(hhd_path).rename(columns=lambda x: x.strip())
    pd_df = pd.read_parquet(pd_path).rename(columns=lambda x: x.strip())
    tr_df = pd.read_parquet(tr_path).rename(columns=lambda x: x.strip())

    combined_df = tr_df.merge(pd_df, on='PRODUCT_NUM').merge(hhd_df, on='HSHD_NUM')
    combined_df['MONTH'] = pd.to_datetime(combined_df['PURCHASE_'], format='%d-%b-%y').dt.month_name()
    combined_df['DATE'] = pd.to_datetime(combined_df['PURCHASE_'], format='%d-%b-%y')
    return combined_df

@cache.memoize(timeout=3600)  # Cache for one hour
def get_data():
    return load_and_combine_data()

df = get_data()

style_header = {'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'}
style_data = {'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'}
style_table = {'height': '300px', 'overflowX': 'auto', 'overflowY': 'auto'}

table = dash_table.DataTable(
    id='table-paging-with-graph',
    columns=[{"name": i, "id": i} for i in df.columns],
    page_size=1000,
    page_action='custom',
    virtualization=True,
    style_data=style_data,
    style_table=style_table,
)

dropdown = dcc.Dropdown(
    id='df-dropdown',
    options=[{'label': x, 'value': x} for x in sorted(df['HSHD_NUM'].unique())],
    value=df['HSHD_NUM'].iloc[0],
    placeholder="Select a Household",
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([dropdown], width={'size': 6}, className='ms-5')
    ]),
    dbc.Row([
        dbc.Col([table], width={'size':7}, className='ms-5 mb-3')
    ])
], fluid=True)

@app.callback(
    Output('table-paging-with-graph', 'data'),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('df-dropdown', 'value')],
     prevent_initial_callback=True
)

def update_table(page_current, page_size, selected_hshd_num):
    if page_current is None:
        page_current = 0
    if page_size is None:
        page_size = 100

    df = get_data()  # Use cached data
    filtered_df = df[df['HSHD_NUM'] == selected_hshd_num]
    sorted_df = filtered_df.sort_values(by=['HSHD_NUM', 'BASKET_NUM', 'DATE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])
    return sorted_df.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')
