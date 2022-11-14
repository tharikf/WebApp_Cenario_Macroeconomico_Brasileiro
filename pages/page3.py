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
    'left' : 840,
    'bottom' : 0,
    'width' : '36rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_23_STYLE = {
    'position' : 'fixed',
    'top' : 520,
    'left' : 1380,
    'bottom' : 0,
    'width' : '36rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}


# Informações #
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
                                                           ep.Media, ep.Minimo, ep.Maximo, ep.Indicador).collect()

    return df_ep


# Cambio Anual #
cambio_total = obtendo_expectativas('Câmbio', entidade_anuais, 30)
def unindo_cambio(x):
    
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

df_cambio_total = unindo_cambio(cambio_total)

fig_prev_cambio = px.bar(df_cambio_total, x = 'Métrica', y = 'Valor', color = 'Anos', barmode = 'group',
                        color_discrete_sequence = ['#03198E', '#04890A'], template = 'plotly_white')

fig_prev_cambio.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas')
fig_prev_cambio.update_yaxes(tickprefix = 'R$')

# Finalizado Cambio Anual #

# Cambio Trimestral #
cambio_trim = obtendo_expectativas('Câmbio', entidade_trimestrais, 30)

def unindo_cambio_tri(x):
    
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

df_cambio_trim = unindo_cambio_tri(cambio_trim)

fig_cambio_trim = px.bar(df_cambio_trim, x = 'Trimestres', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_cambio_trim.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas')

fig_cambio_trim.update_yaxes(tickprefix = 'R$')
# Finalizado Cambio Trimestral #

# Comercio #
def obtendo_expectativas_comercio(indicador, entidade, respondentes):
    
    # Filtrando para previsoes dos ultimos 3 meses
    tres_meses = datetime.date.today() - datetime.timedelta(days = 90)
    tres_meses = tres_meses.strftime('%Y-%m-%d')
    
    # Obtendo dados
    ep = expec.get_endpoint(entidade)
    df_ep = ep.query().filter(ep.Indicador == indicador,
                              ep.Data >= tres_meses,
                              ep.numeroRespondentes >= respondentes).select(ep.Data, ep.DataReferencia,
                                                           ep.Media, ep.Minimo, ep.Maximo, ep.Indicador, ep.IndicadorDetalhe).collect()

    return df_ep

comercio_total = obtendo_expectativas_comercio('Balança comercial', entidade_anuais, 10)

def unindo_bc(x, detalhe):
    
    # Selecionando trimestres
    anos = ['2022', '2023']
    
    x = x[x['DataReferencia'].isin(anos)]
    x = x[x['IndicadorDetalhe'] == detalhe]
    
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

exportacoes_df = unindo_bc(comercio_total, 'Exportações')
importacoes_df = unindo_bc(comercio_total, 'Importações')
saldo_df = unindo_bc(comercio_total, 'Saldo')

fig_prev_expor = px.bar(exportacoes_df, x = 'Métrica', y = 'Valor', color = 'Anos', barmode = 'group',
                        color_discrete_sequence = ['#03198E', '#04890A'], template = 'plotly_white')

fig_prev_expor.update_layout(title = '<br><sup>Valores em Bilhões</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(tick0 = 0, dtick = 50))

fig_prev_expor.update_yaxes(range = (0, 450), constrain = 'domain', tickprefix = 'R$')

fig_prev_impor = px.bar(importacoes_df, x = 'Métrica', y = 'Valor', color = 'Anos', barmode = 'group',
                        color_discrete_sequence = ['#03198E', '#04890A'], template = 'plotly_white')

fig_prev_impor.update_layout(title = '<br><sup>Valores em Bilhões</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas')
fig_prev_impor.update_yaxes(range = (0, 350), constrain = 'domain', tickprefix = 'R$')

fig_prev_saldo = px.bar(saldo_df, x = 'Métrica', y = 'Valor', color = 'Anos', barmode = 'group',
                        color_discrete_sequence = ['#03198E', '#04890A'], template = 'plotly_white')

fig_prev_saldo.update_layout(title = '<br><sup>Valores em Bilhões</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas')
fig_prev_saldo.update_yaxes(range = (0, 100), constrain = 'domain', tickprefix = 'R$')
# Finalizando Comercio #




# Plot das Informacoes
cambio_anual = [
    dbc.CardHeader('Previsões do Câmbio - Anual'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'cambio-prev',
                        figure = fig_prev_cambio,
                        style = {'height' : 360, 'width' : 750}),
        ],
    ),
]

cambio_trimestral = [
    dbc.CardHeader('Previsões do Câmbio - Trimestral'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'cambio-prev-trim',
                        figure = fig_cambio_trim,
                        style = {'height' : 360, 'width' : 750}),
        ],
    ),
]

exportacoes_anual = [
    dbc.CardHeader('Previsões de Exportações'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'expor-prev',
                        figure = fig_prev_expor,
                        style = {'height' : 360, 'width' : 500}),
        ],
    ),
]

importacoes_anual = [
    dbc.CardHeader('Previsões de Importações'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'expor-prev',
                        figure = fig_prev_impor,
                        style = {'height' : 360, 'width' : 500}),
        ],
    ),
]

saldo_anual = [
    dbc.CardHeader('Previsões do Saldo da Balança Comercial'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'expor-prev',
                        figure = fig_prev_saldo,
                        style = {'height' : 360, 'width' : 500}),
        ],
    ),
]

area_informacoes = html.Div(
    [
        html.Div(children = [
            html.Div(children =[
                dbc.Card(cambio_anual),
            ],
            style = DIV_11_STYLE
            ),

            html.Div(children = [
                dbc.Card(cambio_trimestral),
            ],
            style = DIV_12_STYLE
            ),
        ],
        ),

        html.Div(children = [
            html.Div(children = [
                dbc.Card(exportacoes_anual),
            ],
            style = DIV_21_STYLE
            ),

            html.Div(children = [
                dbc.Card(importacoes_anual),
            ],
            style = DIV_22_STYLE
            ),

            html.Div(children = [
                dbc.Card(saldo_anual),
            ],
            style = DIV_23_STYLE
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
