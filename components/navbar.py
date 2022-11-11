from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP, 'seg-style.css']
text_color = {"dark": "#95969A", "light": "#595959"}
card_color = {"dark": "#2D3038", "light": "#FFFFFF"}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 100,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#2D3038",
    'color' : '#FFFFFF',
}

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
                dcc.Link(
                    dbc.Button('Atividade Econômica', color = 'danger', className = 'me-1',
                                style = dict(width = '250px')), href = '/page1', refresh = True
                ),
                html.Br(),
                dcc.Link(
                    dbc.Button('Política Monetária', color = 'danger', className = 'me-1',
                                style = dict(width = '250px')), href = '/page2', refresh = True
                ),
                html.Br(),
                dcc.Link(
                    dbc.Button('Câmbio e Balança Comercial', color = 'danger', className = 'me-1',
                                style = dict(width = '250px')), href = '/page3', refresh = True
                ),
                html.Br(),
                dcc.Link(
                    dbc.Button('Dívida e Investimento', color = 'danger', className = 'me-1', style = dict(width = '250px')), href = '/page4', refresh = True
                ),
                html.Br(),
                dcc.Link(
                    dbc.Button('Voltar para o Início', color = 'danger', className = 'me-1',
                                style = dict(width = '250px')), href = '/', refresh = True
                ),
            ],
            className = 'd-grid gap-2 col-12 mx-auto',
            vertical = True,
        ),
    ],
    style = SIDEBAR_STYLE,
)

def Navbar():

    layout = html.Div(
        [
            header,
            sidebar,
        ]
    )

    return layout



