import dash
from dash import html, dcc, dash_table, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache
from flask import Flask, Blueprint, render_template, render_template_string, redirect, url_for
from src import app as flask_app
import flask
from flask_login import current_user

dash_app = dash.Dash(
    __name__,
    server=flask_app,
    routes_pathname_prefix='/dashboard/',  
    external_stylesheets=[dbc.themes.SLATE]
)

# Securing Dash routes with Flask login
@dash_app.server.before_request
def restrict_dash_access():
    # Check if the request path is for the Dash app
    if '/dashboard/' in flask.request.path:
        # Check if user is not authenticated
        if not current_user.is_authenticated:
            # Redirect to the login page
            return redirect(url_for('accounts.login'))


# Configure Cache
cache = Cache(dash_app.server, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': 'cache-directory'})


# Import Layout and Callback
from .callbacks import register_callbacks
from .layout import layout

# Set layout and register callbacks
dash_app.layout = layout
register_callbacks(dash_app)