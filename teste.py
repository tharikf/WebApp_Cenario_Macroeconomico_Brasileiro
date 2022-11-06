
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from bcb import sgs


# Estilo
external_stylesheets = [dbc.themes.BOOTSTRAP, 'seg-style.css']

# Font and background colors associated with each theme
text_color = {"dark": "#95969A", "light": "#595959"}
card_color = {"dark": "#2D3038", "light": "#FFFFFF"}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 100,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

app = Dash(__name__, external_stylesheets = external_stylesheets)

# Titulo da Aplicacao
app.title = 'Cenário Macroeconômico do Brasil'

# Header
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H3('Cenário Macroeconômico do Brasil'),
                                    html.P('Uma análise atual e previsões para 2023!'),
                                ],
                                id = 'app-title',
                                style = {
                                    'color' : 'white',
                                }
                            )
                        ],
                        md = True,
                        align = 'left',
                    ),

                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.P('Essa é uma aplicação com indicadores macroeconômicos brasileiros. '
                                            'Aqui é possível observar indicadores como taxa selic, inflação, câmbio e desemprego. '
                                            'Além disso, a aplicação conta com previsões das principais instituições financeiras fornecidas do país '
                                             'compondo as expectativas do COPOM sobre os principais indicadores para o ano de 2023!'),
                                ],
                                id = 'app-descricao',
                                style = {
                                    'color' : 'white',
                                    'text-align': 'left',
                                }
                            )
                        ],
                        md = True,
                        align = 'right',
                    ),
                ],
                align = 'center',
            ),
        ],
        fluid = True,
    ),
    dark = True,
    color = 'dark',
    sticky = 'top',
)

# Side-Bar
sidebar = html.Div(
    [
        html.H2('Indicadores', className = 'display-5'),
        html.Hr(),
        html.P('Escolha o indicador que deseja ver!'),

        dbc.Nav(
            [
                dbc.Button('PIB', color = 'primary', className = 'me-1'),
                html.Br(),
                dbc.Button('Inflação', color = 'secondary', className = 'me-1'),
                html.Br(),
                dbc.Button('Juros', color = 'success', className = 'me-1'),
                html.Br(),
                dbc.Button('Desemprego', color = 'warning', className = 'me-1'),
            ],
            className = 'd-grid gap-2 col-12 mx-auto',
            vertical = True,
        ),
    ],
    style = SIDEBAR_STYLE,
)

# Area de plotagem
pib_content = [
    dbc.CardHeader('PIB'),
    dbc.CardBody(
        [
            html.H5('PIB 2022', className = 'card-title'),
            html.P(
                'Aqui estarão as infomações do PIB do Brasil!',
                className = 'card-text',
            ),
        ]
    ),
]

inflacao_content = [
    dbc.CardHeader('Inflação'),
    dbc.CardBody(
        [
            html.H5('Inflação 2022', className = 'card-title'),
            html.P(
                'Aqui estarão as infomações de inflação do Brasil!',
                className = 'card-text',
            ),
        ]
    ),
]

juros_content = [
    dbc.CardHeader('Taxa de Juros'),
    dbc.CardBody(
        [
            html.H5('Taxa de Juros 2022', className = 'card-title'),
            html.P(
                'Aqui estarão as infomações de taxa de juros do Brasil!',
                className = 'card-text',
            ),
        ]
    ),
]

desemprego_content = [
    dbc.CardHeader('Desemprego'),
    dbc.CardBody(
        [
            html.H5('Desemprego 2022', className = 'card-title'),
            html.P(
                'Aqui estarão as infomações de taxa de desemprego do Brasil!',
                className = 'card-text',
            ),
        ]
    ),
]



# Layout
app.layout = html.Div(
    [
        header,
        dbc.Container(
            [
                dbc.Row(
                    sidebar
                    ),
            ],
            fluid = True,
        ),
    ],
)



#  Executa o programa
if __name__ == '__main__':
    app.run_server(debug = False, threaded = True)