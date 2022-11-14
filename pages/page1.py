# Import necessary libraries 
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
from bcb import sgs
from bcb import currency
from bcb import Expectativas
from decimal import *

##### PAGINA PIB #####

# Estilo
external_stylesheets = [dbc.themes.BOOTSTRAP, 'seg-style.css']

# Font and background colors associated with each theme
text_color = {"dark": "#95969A", "light": "#595959"}
card_color = {"dark": "#2D3038", "light": "#FFFFFF"}

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
    'left' : 1085,
    'bottom' : 412,
    'width' : '54rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_21_STYLE = {
    'position' : 'fixed',
    'top' : 515,
    'left' : 288,
    'bottom' : 10,
    'width' : '26rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_22_STYLE = {
    'position' : 'fixed',
    'top' : 515,
    'left' : 695,
    'bottom' : 10,
    'width' : '26rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_23_STYLE = {
    'position' : 'fixed',
    'top' : 515,
    'left' : 1100,
    'bottom' : 10,
    'width' : '26rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_24_STYLE = {
    'position' : 'fixed',
    'top' : 515,
    'left' : 1510,
    'bottom' : 10,
    'width' : '26rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}
# Informacoes

# Funcoes Auxiliares
expec = Expectativas()
entidade_anuais = 'ExpectativasMercadoAnuais'
entidade_trimestrais = 'ExpectativasMercadoTrimestrais'

def obtendo_expectativas(indicador, entidade, respondentes):
    
    # Filtrando para previsoes dos ultimos 3 meses
    tres_meses = datetime.date.today() - datetime.timedelta(days = 90)
    tres_meses = tres_meses.strftime('%Y-%m-%d')
    
    # Obtendo dados
    ep = expec.get_endpoint(entidade)
    df_ep = ep.query().filter(ep.Indicador == indicador,
                              ep.Data >= tres_meses,
                              ep.numeroRespondentes >= respondentes).select(ep.Data, ep.DataReferencia,
                                                           ep.Media, ep.Mediana, ep.Maximo, ep.Minimo).collect()

    return df_ep

def unindo_prev(x):
    
    # Selecionando trimestres
    trimestres = ['4/2022', '1/2023', '2/2023', '3/2023', '4/2023']
    
    # Calculando as metricas
    dicio_metricas = {}
    df_aux = x.copy()
    for trimestre in trimestres:
        df_aux = x[(x['DataReferencia'] == trimestre)]
        dicio_metricas['media_{}'.format(trimestre)] = df_aux['Media'].mean()
        dicio_metricas['maximo_{}'.format(trimestre)] = df_aux['Maximo'].mean()
        dicio_metricas['minimo_{}'.format(trimestre)] = df_aux['Minimo'].mean()
    
    # Colocando em um dataframe
    df = pd.DataFrame(list(dicio_metricas.items()))
    df.columns = ['metrica_trimestre', 'valor']
    df[['metrica', 'trimestres']] = df['metrica_trimestre'].str.split('_', n = 1, expand = True)
    df = df.drop(columns = 'metrica_trimestre')
    df = df[['trimestres', 'metrica', 'valor']]
    df.columns = ['Trimestres', 'Métrica', 'Valor']
    df['Valor'] = round(df['Valor'], 2)
    df['Métrica'] = np.where(df['Métrica'] == 'maximo', 'Máximo',
                              np.where(df['Métrica'] == 'media', 'Média', 'Mínimo'))
    
    return df

# PIB e DESEMPREGO PREVISOES #

# Desemprego #
# Desemprego Anual
desemprego_total = obtendo_expectativas('Taxa de desocupação', entidade_anuais, 30)

def unindo_desemprego(x):
    
    # Selecionando trimestres
    anos = ['2022', '2023']
    
    x = x[x['DataReferencia'].isin(anos)]
    
    # Calculando as metricas
    dicio_metricas = {}
    df_aux = x.copy()
    for ano in df_aux['DataReferencia']:
        df_aux = x[(x['DataReferencia'] == ano)]
        dicio_metricas['media_{}'.format(ano)] = df_aux['Media'].mean()
        dicio_metricas['maximo_{}'.format(ano)] = df_aux['Maximo'].mean()
        dicio_metricas['minimo_{}'.format(ano)] = df_aux['Minimo'].mean()
    
    # Colocando em um dataframe
    df = pd.DataFrame(list(dicio_metricas.items()))
    df.columns = ['metrica_trimestre', 'valor']
    df[['metrica', 'anos']] = df['metrica_trimestre'].str.split('_', n = 1, expand = True)
    df = df.drop(columns = 'metrica_trimestre')
    df = df[['anos', 'metrica', 'valor']]
    df.columns = ['Anos', 'Métrica', 'Valor']
    df['Valor'] = round(df['Valor'], 2)
    df['Métrica'] = np.where(df['Métrica'] == 'maximo', 'Máximo',
                              np.where(df['Métrica'] == 'media', 'Média', 'Mínimo'))
    
    return df

df_desemprego_anual = unindo_desemprego(desemprego_total)

fig_prev_desemp_anual = px.bar(df_desemprego_anual, x = 'Métrica', y = 'Valor', color = 'Anos', barmode = 'group',
                        color_discrete_sequence = ['#03198E', '#04890A'], template = 'plotly_white')

fig_prev_desemp_anual.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Anos', yaxis = dict(dtick = 1))

fig_prev_desemp_anual.update_yaxes(range = (0, 12), constrain = 'domain', ticksuffix = '%')
# Finalizado Desemprego Anual

# Desemprego Trimestral
desemprego_total_tri = obtendo_expectativas('Taxa de desocupação', entidade_trimestrais, 30)

desemprego_total_tri_df = unindo_prev(desemprego_total_tri)

fig_prev_desemp_tri = px.bar(desemprego_total_tri_df, x = 'Trimestres', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_prev_desemp_tri.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(dtick = 1))
fig_prev_desemp_tri.update_yaxes(range = (0, 13), constrain = 'domain', ticksuffix = '%')
# Finalizando Desemprego Trimestral

# Finalizando Desemprego #

# PIB Trimestrais #
# Pelo menos 30 respondentes!
pib_total = obtendo_expectativas('PIB Total', entidade_trimestrais, 30)
df_previsoes_pib = unindo_prev(pib_total)

fig_prev_pib = px.bar(df_previsoes_pib, x = 'Trimestres', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')
fig_prev_pib.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(dtick = 1))
fig_prev_pib.update_yaxes(range = (-5, 5), constrain = 'domain', ticksuffix = '%')
# Finalizando PIB Trimestrais #

# PIB Anual #
# Pelo menos 30 respondentes!
pib_total = obtendo_expectativas('PIB Total', entidade_anuais, 30)
pib_2022_media = round(pib_total[pib_total['DataReferencia'] == '2022']['Media'].mean(), 2)
pib_2023_media = round(pib_total[pib_total['DataReferencia'] == '2023']['Media'].mean(), 2)

pib_2022_fig = go.Figure()
pib_2022_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2022_media,
title = 'PIB 2022',
))

pib_2023_fig = go.Figure()
pib_2023_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2023_media,
title = 'PIB 2023',
))
# Finalizando PIB Anual #

# PIB por setores #
# Pelo menos 30 respondentes!
# Agro
pib_agro = obtendo_expectativas('PIB Agropecuária', entidade_anuais, 30)
pib_2022_agro = round(pib_agro[pib_agro['DataReferencia'] == '2022']['Media'].mean(), 2)
pib_2023_agro = round(pib_agro[pib_agro['DataReferencia'] == '2023']['Media'].mean(), 2)

pib_2022_agro_fig = go.Figure()
pib_2022_agro_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2022_agro,
title = 'PIB - Agropecuária: 2022',
))

pib_2023_agro_fig = go.Figure()
pib_2023_agro_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2023_agro,
title = 'PIB - Agropecuária: 2023',
))

# Industria
pib_ind = obtendo_expectativas('PIB Indústria', entidade_anuais, 30)
pib_2022_ind = round(pib_ind[pib_ind['DataReferencia'] == '2022']['Media'].mean(), 2)
pib_2023_ind = round(pib_ind[pib_ind['DataReferencia'] == '2023']['Media'].mean(), 2)

pib_2022_ind_fig = go.Figure()
pib_2022_ind_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2022_ind,
title = 'PIB - Indústria: 2022',
))

pib_2023_ind_fig = go.Figure()
pib_2023_ind_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2023_ind,
title = 'PIB - Indústria: 2023',
))


# Servicos
pib_servicos = obtendo_expectativas('PIB Serviços', entidade_anuais, 30)
pib_2022_serv = round(pib_servicos[pib_servicos['DataReferencia'] == '2022']['Media'].mean(), 2)
pib_2023_serv = round(pib_servicos[pib_servicos['DataReferencia'] == '2023']['Media'].mean(), 2)

pib_2022_serv_fig = go.Figure()
pib_2022_serv_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2022_serv,
title = 'PIB - Serviços: 2022',
))

pib_2023_serv_fig = go.Figure()
pib_2023_serv_fig.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = pib_2023_serv,
title = 'PIB - Serviços: 2023',
))

# Finalizando PIB por setores #

# Plot das Informacoes
desemp_anual = [
    dbc.CardHeader('Previsões para o Desemprego'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'desemp-2022',
                                figure = fig_prev_desemp_anual,
                                style = {'height' : 360, 'width' : 800}),
        ), label = 'Desemprego Anual'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'desemp-2023',
                                figure = fig_prev_desemp_tri,
                                style = {'height' : 360, 'width' : 800}),
        ), label = 'Desemprego Trimestral'
            ),
        ]
    )
]

pib_trimestres = [
    dbc.CardHeader('Previsões do PIB - Trimestral'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'pib-trim-previsoes',
                        figure = fig_prev_pib,
                        style = {'height' : 360, 'width' : 760}),
        ],
    ),
]

pib_anuais = [
    dbc.CardHeader('Previsões para o PIB - Anual'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-2022',
                                figure = pib_2022_fig,
                                style = {'height' : 300}),
        ), label = 'Previsão PIB 2022'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-2023',
                                figure = pib_2023_fig,
                                style = {'height' : 300}),
        ), label = 'Previsão PIB 2023'
            ),
        ]
    )
]

pib_agropec = [
    dbc.CardHeader('Previsões para o PIB - Agropecuária'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-agropec-2022',
                                figure = pib_2022_agro_fig,
                                style = {'height' : 300}),
        ), label = 'Agropecuária - 2022'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-agropec-2023',
                                figure = pib_2023_agro_fig,
                                style = {'height' : 300}),
        ), label = 'Agropecuária - 2023'
            ),
        ]
    )
]

pib_indust = [
    dbc.CardHeader('Previsões para o PIB - Indústria'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-industria-2022',
                                figure = pib_2022_ind_fig,
                                style = {'height' : 300}),
        ), label = 'Indústria - 2022'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-industria-2023',
                                figure = pib_2023_ind_fig,
                                style = {'height' : 300}),
        ), label = 'Indústria - 2023'
            ),
        ]
    )
]

pib_servic = [
    dbc.CardHeader('Previsões para o PIB - Serviços'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-servic-2022',
                                figure = pib_2022_serv_fig,
                                style = {'height' : 300}),
        ), label = 'Serviços - 2022'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'pib-servic-2023',
                                figure = pib_2023_serv_fig,
                                style = {'height' : 300}),
        ), label = 'Serviços - 2023'
            ),
        ]
    )
]


area_informacoes = html.Div(
    [
        html.Div(children = [
            html.Div(children =[
                dbc.Card(pib_trimestres),
            ],
            style = DIV_11_STYLE
            ),

            html.Div(children = [
                dbc.Card(desemp_anual),
            ],
            style = DIV_12_STYLE
            ),
        ],
        ),

        html.Div(children = [
            html.Div(children = [
                dbc.Card(pib_anuais),
            ],
            style = DIV_21_STYLE
            ),

            html.Div(children = [
                dbc.Card(pib_agropec),
            ],
            style = DIV_22_STYLE
            ),

            html.Div(children = [
                dbc.Card(pib_indust),
            ],
            style = DIV_23_STYLE
            ),

            html.Div(children = [
                dbc.Card(pib_servic),
            ],
            style = DIV_24_STYLE
            ),
        ],
        ),
    ],
)

# Layout
layout = html.Div(
    [
        area_informacoes,
    ]
)

