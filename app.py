from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                suppress_callback_exceptions=True)

server = app.server
