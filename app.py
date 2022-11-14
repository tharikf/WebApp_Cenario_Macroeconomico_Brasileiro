from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags = [{'name': 'viewport', "content" : "width=device-width, initial-scale=0.19, maximum-scale=5, minimum-scale=0.1, device-height=50"}],
                suppress_callback_exceptions=True)
                
