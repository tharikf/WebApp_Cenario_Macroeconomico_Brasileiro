from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
from bcb import sgs
from bcb import currency
from bcb import Expectativas
import yfinance as yf

# Estilo
external_stylesheets = [dbc.themes.BOOTSTRAP, 'seg-style.css']

# Titulo da Aplicacao
#app.title = 'Cenário Macroeconômico do Brasil'

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
    "background-color": "#2D3038",
    'color' : '#FFFFFF',
}

DIV_11_STYLE = {
    'position' : 'fixed',
    'top' : 100,
    'left' : 288,
    'bottom' : 412,
    'width' : '54rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_12_STYLE = {
    'position' : 'fixed',
    'top' : 100,
    'left' : 1070,
    'bottom' : 412,
    'width' : '54rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_21_STYLE = {
    'position' : 'fixed',
    'top' : 520,
    'left' : 288,
    'bottom' : 0,
    'width' : '36rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_22_STYLE = {
    'position' : 'fixed',
    'top' : 520,
    'left' : 830,
    'bottom' : 0,
    'width' : '36rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_23_STYLE = {
    'position' : 'fixed',
    'top' : 520,
    'left' : 1345,
    'bottom' : 0,
    'width' : '36rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
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
                dbc.Button('PIB', color = 'danger', className = 'me-1'),
                html.Br(),
                dbc.Button('Inflação', color = 'danger', className = 'me-1'),
                html.Br(),
                dbc.Button('Juros', color = 'danger', className = 'me-1'),
                html.Br(),
                dbc.Button('Desemprego', color = 'danger', className = 'me-1'),
                html.Br(),
                dbc.Button('Câmbio', color = 'danger', className = 'me-1'),
            ],
            className = 'd-grid gap-2 col-12 mx-auto',
            vertical = True,
        ),
    ],
    style = SIDEBAR_STYLE,
)

# PIB (IBC-BR) #
df_pib = sgs.get({'ibcbr' : 24363}, start = '2022-01-01')
df_pib = df_pib.reset_index()

pib_figure = go.Figure()
pib_figure = px.line(x = df_pib['Date'], y = df_pib['ibcbr'], color_discrete_sequence = ['#1E3685'], template = 'plotly_white')
pib_figure.update_layout(title = 'Série Temporal do IBC-BR', title_x = 0.5, xaxis_title = '', yaxis_title = '')
# Finalizando PIB #

# Inflacao (IPCA) #
inflacao = sgs.get({'ipca' : 433, 'igp-m' : 189, 'inpc' : 188}, start = '2021-01-01')

def inflacao_ipca_anual(df_inflacao):
    inflacao_df = df_inflacao.copy()
    inflacao_df = inflacao_df.reset_index()
    inflacao_df = inflacao_df.dropna().tail(13)
    
    # acumulando IPCA
    inflacao_ipca = inflacao_df[['Date', 'ipca']]
    inflacao_ipca = inflacao_ipca.assign(ipca_indice = False)
    for i in inflacao_ipca.loc[1:, 'ipca_indice']:
        inflacao_ipca['ipca_indice'] = (inflacao_ipca['ipca'] / 100) + 1
    
    inflacao_ipca.iloc[0, -1] = 1
    inflacao_ipca['ipca_acumulado'] = np.cumprod(inflacao_ipca['ipca_indice'])
    
    inflacao_12meses_ipca = inflacao_ipca['ipca_acumulado'].tail(1).item()
    inflacao_12meses_ipca = round((inflacao_12meses_ipca - 1) * 100, 2)
    
    # acumulando IGP-M
    inflacao_igpm = inflacao_df[['Date', 'igp-m']]
    inflacao_igpm = inflacao_igpm.assign(igpm_indice = False)
    for i in inflacao_igpm.loc[1:, 'igpm_indice']:
        inflacao_igpm['igpm_indice'] = (inflacao_igpm['igp-m'] / 100) + 1
    
    inflacao_igpm.iloc[0, -1] = 1
    inflacao_igpm['igpm_acumulado'] = np.cumprod(inflacao_igpm['igpm_indice'])
    
    inflacao_12meses_igpm = inflacao_igpm['igpm_acumulado'].tail(1).item()
    inflacao_12meses_igpm = round((inflacao_12meses_igpm - 1) * 100, 2)
    
    # acumulando inpc
    inflacao_inpc = inflacao_df[['Date', 'inpc']]
    inflacao_inpc = inflacao_inpc.assign(inpc_indice = False)
    for i in inflacao_inpc.loc[1:, 'inpc_indice']:
        inflacao_inpc['inpc_indice'] = (inflacao_inpc['inpc'] / 100) + 1
    
    inflacao_inpc.iloc[0, -1] = 1
    inflacao_inpc['inpc_acumulado'] = np.cumprod(inflacao_inpc['inpc_indice'])
    
    inflacao_12meses_inpc = inflacao_inpc['inpc_acumulado'].tail(1).item()
    inflacao_12meses_inpc = round((inflacao_12meses_inpc - 1) * 100, 2)
    
    
    return inflacao_12meses_ipca, inflacao_12meses_igpm, inflacao_12meses_inpc

ipca_anualizado = inflacao_ipca_anual(inflacao)[0]
igpm_anualizado = inflacao_ipca_anual(inflacao)[1]
inpc_anualizado = inflacao_ipca_anual(inflacao)[2]

taxas_ipca = go.Figure()
taxas_ipca.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%'},
value = ipca_anualizado,
title = 'IPCA',
))

taxas_igpm = go.Figure()
taxas_igpm.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%'},
value = igpm_anualizado,
title = 'IGP-M',
))

taxas_inpc = go.Figure()
taxas_inpc.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%'},
value = inpc_anualizado,
title = 'INPC',
))
# Finalizando Inflacao #

# Juros (Selic e TJLP) #
# Selic
tx_selic = sgs.get({'selic' : 432}, start = '2022-01-01')
tx_selic = tx_selic.reset_index()
selic_atual = tx_selic['selic'].tail(1).item()

#TJLP
tx_tjlp = sgs.get({'tjlp' : 256}, start = '2022-01-01')
juros_LP = tx_tjlp['tjlp'].tail(1).item()

taxa_selic = go.Figure()
taxa_selic.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%'},
value = selic_atual,
title = 'Taxa Selic',
))

taxa_tjlp = go.Figure()
taxa_tjlp.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = juros_LP,
title = 'Taxa de Juros de Longo Prazo',
))
# Finalizado Juros #

# Desemprego (PNADC) #
df_desemprego = sgs.get({'desemp_pnadc' : 24369}, start = '2022-01-01')
df_desemprego = df_desemprego.reset_index()
desemprego_figure = px.line(x = df_desemprego['Date'], y = df_desemprego['desemp_pnadc'], color_discrete_sequence = ['#1E3685'],
                            template = 'plotly_white')
desemprego_figure.update_layout(title = 'Série Temporal do Desemprego', title_x = 0.5, xaxis_title = '',
                                yaxis_title = 'Taxa de Desemprego')

# Finalizando Desemprego #

# Cambio #
# Um dia na frente por causa do python fazendo o range + 1
hoje = datetime.date.today()
inicio = hoje - datetime.timedelta(days = 7)
fim = hoje + datetime.timedelta(days = 1)
moedas_busca = 'USDBRL=X EURBRL=X GBPBRL=X'

# Pelo yfinance é mais recente
def obtendo_cambio(moedas, data_inicio, data_final):
    df = yf.download(moedas, start = data_inicio, end = data_final, progress = False)
    df = df[['Adj Close']].reset_index()
    df.columns = df.columns.droplevel(0)
    df = df.rename(columns = {'' :'Data'})
    dolar = round(df['USDBRL=X'].tail(1).item(), 2)
    euro = round(df['EURBRL=X'].tail(1).item(), 2)
    libra = round(df['GBPBRL=X'].tail(1).item(), 2)
    return dolar, euro, libra

dolar_hoje = obtendo_cambio(moedas_busca, inicio, fim)[0]
euro_hoje = obtendo_cambio(moedas_busca, inicio, fim)[1]
libra_hoje = obtendo_cambio(moedas_busca, inicio, fim)[2]

dolar_fig = go.Figure()
dolar_fig.add_trace(go.Indicator(
mode = 'number',
number = {'prefix' : 'R$'},
value = dolar_hoje,
title = 'Cotação Dólar',
))

euro_fig = go.Figure()
euro_fig.add_trace(go.Indicator(
mode = 'number',
number = {'prefix' : 'R$'},
value = euro_hoje,
title = 'Cotação Euro',
))

libra_fig = go.Figure()
libra_fig.add_trace(go.Indicator(
mode = 'number',
number = {'prefix' : 'R$'},
value = libra_hoje,
title = 'Cotação Libra Esterlina',
))


# Finalizando Cambio #


# Area de plotagem
pib_content = [
    dbc.CardHeader('Atividade Econômica'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'pib-ibcbr',
                        figure = pib_figure,
                        style = {'height' : 360, 'width' : 750}),
        ],
    ),
]

inflacao_content = [
    dbc.CardHeader('Inflação - Últimos 12 Meses'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'taxa-IPCA',
                                figure = taxas_ipca,
                                style = {'height' : 300}),
        ), label = 'IPCA'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'taxa-IGPM',
                                figure = taxas_igpm,
                                style = {'height' : 300}),
        ), label = 'IGP-M'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'taxa-INPC',
                                figure = taxas_inpc,
                                style = {'height' : 300}),
                ), label = 'INPC'
            ),
        ]
    )
    
]

juros_content = [
    dbc.CardHeader('Taxa de Juros Atualmente'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'taxa-selic',
                                figure = taxa_selic,
                                style = {'height' : 300}),
        ), label = 'Selic'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'taxa-tjlp',
                                figure = taxa_tjlp,
                                style = {'height' : 300}),
        ), label = 'Juros de Longo Prazo'
            ),
        ]
    )
    
]

desemprego_content = [
    dbc.CardHeader('Taxa de Desemprego'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'taxa-desemprego',
            figure = desemprego_figure,
            style = {'height' : 360, 'width' : 750}),
        ]
    ),
]

cambio_content = [
    dbc.CardHeader('Câmbio Hoje'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'fig-dolar',
                                figure = dolar_fig,
                                style = {'height' : 300}),
        ), label = 'Dólar'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'fig-euro',
                                figure = euro_fig,
                                style = {'height' : 300}),
        ), label = 'Euro'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'fig-libra',
                                figure = libra_fig,
                                style = {'height' : 300}),
                ), label = 'Libra Esterlina'
            ),
        ]
    )
    
]

area_informacoes = html.Div(
    [
        html.Div(children = [
            html.Div(children =[
                dbc.Card(pib_content),
            ],
            style = DIV_11_STYLE
            ),

            html.Div(children = [
                dbc.Card(desemprego_content),
            ],
            style = DIV_12_STYLE
            ),
        ],
        ),

        html.Div(children = [
            html.Div(children = [
                dbc.Card(juros_content),
            ],
            style = DIV_21_STYLE
            ),

            html.Div(children = [
                dbc.Card(inflacao_content),
            ],
            style = DIV_22_STYLE
            ),

            html.Div(children = [
                dbc.Card(cambio_content),
            ],
            style = DIV_23_STYLE
            ),
        ],
        ),
    ],
)

# Layout
def pagprin():
    
    layout = html.Div(
        [
            area_informacoes,
        ]
    )
    return layout


