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
    'left' : 1100,
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
    'width' : '70rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_22_STYLE = {
    'position' : 'fixed',
    'top' : 515,
    'left' : 1280,
    'bottom' : 10,
    'width' : '40rem',
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
        dicio_metricas['mediana_{}'.format(trimestre)] = df_aux['Mediana'].mean()
        dicio_metricas['maximo_{}'.format(trimestre)] = df_aux['Maximo'].mean()
        dicio_metricas['minimo_{}'.format(trimestre)] = df_aux['Minimo'].mean()
    
    # Colocando em um dataframe
    df = pd.DataFrame(list(dicio_metricas.items()))
    df.columns = ['metrica_trimestre', 'valor']
    df[['metrica', 'trimestres']] = df['metrica_trimestre'].str.split('_', n = 1, expand = True)
    df = df.drop(columns = 'metrica_trimestre')
    df = df[['trimestres', 'metrica', 'valor']]
    df['metrica'] = np.where(df['metrica'] == 'maximo', 'Máximo',
                              np.where(df['metrica'] == 'media', 'Média',
                                       np.where(df['metrica'] == 'minimo', 'Mínimo', 'Mediana')))
    
    return df

# INFLACAO E JUROS PREVISOES #

# SELIC Anual #
selic_total = obtendo_expectativas('Selic', entidade_anuais, 30)

def unindo_selic(x):
    
    # Selecionando trimestres
    anos = ['2022', '2023']
    
    x = x[x['DataReferencia'].isin(anos)]
    
    # Calculando as metricas
    dicio_metricas = {}
    df_aux = x.copy()
    for ano in df_aux['DataReferencia']:
        df_aux = x[(x['DataReferencia'] == ano)]
        dicio_metricas['media_{}'.format(ano)] = df_aux['Media'].mean()
        dicio_metricas['mediana_{}'.format(ano)] = df_aux['Mediana'].mean()
        dicio_metricas['maximo_{}'.format(ano)] = df_aux['Maximo'].mean()
        dicio_metricas['minimo_{}'.format(ano)] = df_aux['Minimo'].mean()
    
    # Colocando em um dataframe
    df = pd.DataFrame(list(dicio_metricas.items()))
    df.columns = ['metrica_trimestre', 'valor']
    df[['metrica', 'anos']] = df['metrica_trimestre'].str.split('_', n = 1, expand = True)
    df = df.drop(columns = 'metrica_trimestre')
    df = df[['anos', 'metrica', 'valor']]
    
    df['metrica'] = np.where(df['metrica'] == 'maximo', 'Máximo',
                              np.where(df['metrica'] == 'media', 'Média',
                                       np.where(df['metrica'] == 'minimo', 'Mínimo', 'Mediana')))
    
    return df

selic_total_df = unindo_selic(selic_total)

fig_prev_selic = px.bar(selic_total_df, x = 'metrica', y = 'valor', color = 'anos', barmode = 'group',
                        color_discrete_sequence = ['#03198E', '#04890A'], template = 'plotly_white')

fig_prev_selic.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(dtick = 2))
fig_prev_selic.update_yaxes(range = (0, 16), constrain = 'domain', ticksuffix = '%')
# Finalizando SELIC Anual


# IPCA Trimestrais #
ipca_total = obtendo_expectativas('IPCA', entidade_trimestrais, 30)
df_previsoes_ipca = unindo_prev(ipca_total)

fig_prev_ipca = px.bar(df_previsoes_ipca, x = 'trimestres', y = 'valor', color = 'metrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#069099', '#080699', '#E41006'], template = 'plotly_white')

fig_prev_ipca.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas')
fig_prev_ipca.update_yaxes(range = (0, 4), constrain = 'domain', ticksuffix = '%')
# Finalizado IPCA Trimestrais #

# IPCA Decompondo Trimestrais #
def obtendo_expectativas_varios(entidade, respondentes):
    
    # Filtrando para previsoes dos ultimos 3 meses
    tres_meses = datetime.date.today() - datetime.timedelta(days = 90)
    tres_meses = tres_meses.strftime('%Y-%m-%d')
    
    # Obtendo dados
    ep = expec.get_endpoint(entidade)
    df_ep = ep.query().filter(ep.Data >= tres_meses,
                              ep.numeroRespondentes >= respondentes).select().collect()

    return df_ep

def ipca_grupos_func(x):
    
    indicadores = ['IPCA Administrados', 'IPCA Livres', 'IPCA Alimentação no domicílio',
                   'IPCA Serviços', 'IPCA Bens industrializados']

    trimestres = ['4/2022', '1/2023', '2/2023', '3/2023', '4/2023']
    
    x = x[x['Indicador'].isin(indicadores)]
    x = x[x['DataReferencia'].isin(trimestres)]
    x_media = x.groupby(['Indicador', 'DataReferencia'], as_index = False)['Media'].mean()
    x_media['Indicador'] = np.where(x_media['Indicador'] == 'IPCA Bens industrializados', 'IPCA Bens Industrializados',
                                   np.where(x_media['Indicador'] == 'IPCA Alimentação no domicílio','IPCA Alimentação: Domicílio',
                                           x_media['Indicador']))
    return x_media

ipca_grupos = obtendo_expectativas_varios(entidade_trimestrais, 30)
df_ipca_grupos = ipca_grupos_func(ipca_grupos)

ipca_varios_figure = go.Figure()
ipca_varios_figure = px.bar(df_ipca_grupos, x = 'DataReferencia', y = 'Media',
                                color = 'Indicador', 
                                color_discrete_map = {
                                    'IPCA Administrados':'#041367', 'IPCA Alimentação no domicílio':'#0D6F06',
                                    'IPCA Bens industrializados':'#5F066F', 'IPCA Livres':'#A47B1C',
                                    'IPCA Serviços':'#A41C1C'}, template = 'plotly_white')

ipca_varios_figure.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '', yaxis = dict(dtick = 1))
#ipca_varios_figure.update_xaxes(categoryorder = 'array', categoryarray= ['4/2022', '1/2023', '2/2023', '3/2023', '4/2023'])
ipca_varios_figure.update_yaxes(range = (0, 10), constrain = 'domain', ticksuffix = '%')
# Finalizado IPCA Decompondo Trimestrais #

# IPCA Decompondo Anuais #
ipca_gp_anual = obtendo_expectativas_varios(entidade_anuais, 30)
def ipca_gp_ano_func(x):
    
    indicadores = ['IPCA Administrados', 'IPCA Livres', 'IPCA Alimentação no domicílio',
                   'IPCA Serviços', 'IPCA Bens industrializados']
    
    anos = ['2022', '2023']

    x = x[x['Indicador'].isin(indicadores)]
    x = x[x['DataReferencia'].isin(anos)]
    x_media = x.groupby(['Indicador', 'DataReferencia'], as_index = False)['Media'].mean()
    x_media['Indicador'] = np.where(x_media['Indicador'] == 'IPCA Bens industrializados', 'IPCA Bens Industrializados',
                                   np.where(x_media['Indicador'] == 'IPCA Alimentação no domicílio','IPCA Alimentação: Domicílio',
                                           x_media['Indicador']))
    return x_media

df_ipca_gp_anual = ipca_gp_ano_func(ipca_gp_anual)

ipca_gp_anual_figure = go.Figure()
ipca_gp_anual_figure = px.bar(df_ipca_gp_anual, x = 'Indicador', y = 'Media', color = 'DataReferencia', barmode = 'group',
                                color_discrete_sequence = ['#180575', '#04890A'], template = 'plotly_white')
ipca_gp_anual_figure.update_layout(title = '', title_x = 0.5, xaxis_title = '', yaxis_title = '%', yaxis = dict(dtick = 2))
ipca_gp_anual_figure.update_yaxes(range = (-5, 15), constrain = 'domain', ticksuffix = '%')
# Finalizando IPCA Decompondo Anuais

# IPCA E IGP-M Anuais #
ipca_anual_22 = ipca_gp_anual[(ipca_gp_anual['Indicador'] == 'IPCA') & (ipca_gp_anual['DataReferencia'] == '2022')]['Media'].mean()
ipca_anual_23 = ipca_gp_anual[(ipca_gp_anual['Indicador'] == 'IPCA') & (ipca_gp_anual['DataReferencia'] == '2023')]['Media'].mean()

igpm_anual_22 = ipca_gp_anual[(ipca_gp_anual['Indicador'] == 'IGP-M') & (ipca_gp_anual['DataReferencia'] == '2022')]['Media'].mean()
igpm_anual_23 = ipca_gp_anual[(ipca_gp_anual['Indicador'] == 'IGP-M') & (ipca_gp_anual['DataReferencia'] == '2023')]['Media'].mean()

ipca_anual_22_figu = go.Figure()
ipca_anual_22_figu.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = ipca_anual_22,
title = 'IPCA: 2022',
))

ipca_anual_23_figu = go.Figure()
ipca_anual_23_figu.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = ipca_anual_23,
title = 'IPCA: 2023',
))

igpm_anual_22_figu = go.Figure()
igpm_anual_22_figu.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = igpm_anual_22,
title = 'IGP-M: 2022',
))

igpm_anual_23_figu = go.Figure()
igpm_anual_23_figu.add_trace(go.Indicator(
mode = 'number',
number = {'suffix' : '%', 'valueformat' : '.2f'},
value = igpm_anual_23,
title = 'IGP-M: 2023',
))

# Finalizando IPCA e IGP-M Anuais #



# Plot das Informacoes
selic_anual = [
    dbc.CardHeader('Previsões da SELIC'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'selic-prev',
                        figure = fig_prev_selic,
                        style = {'height' : 360, 'width' : 750}),
        ],
    ),
]

inflacao_trimestrais_gps = [
    dbc.CardHeader('Previsões para Inflação - Trimestrais'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'inf-grupos-prev',
                                figure = ipca_varios_figure,
                                style = {'height' : 300, 'width' : 800}),
        ), label = 'IPCA Trimestral por Grupos'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'inf-totais-prev',
                                figure = fig_prev_ipca,
                                style = {'height' : 300, 'width' : 800}),
        ), label = 'IPCA Trimestral Total'
            ),
        ],
    ),
]

ipca_grupos_anuais = [
    dbc.CardHeader('Previsões do IPCA por Grupos - Anual'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'ipca-grupos-anual-previsoes',
                        figure = ipca_gp_anual_figure,
                        style = {'height' : 380, 'width' : 900}),
        ],
    ),
]

inflacao_anuais_ipca_igpm = [
    dbc.CardHeader('Previsões para Inflação'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'ipca-2022-card',
                                figure = ipca_anual_22_figu,
                                style = {'height' : 300}),
        ), label = 'IPCA: 2022'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'ipca-2023-card',
                                figure = ipca_anual_23_figu,
                                style = {'height' : 300}),
        ), label = 'IPCA: 2023'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'igpm-2022-card',
                                figure = igpm_anual_22_figu,
                                style = {'height' : 300}),
        ), label = 'IGP-M: 2022'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'igpm-2023-card',
                                figure = igpm_anual_23_figu,
                                style = {'height' : 300}),
        ), label = 'IGP-M: 2023'
            ),
        ]
    )
]

area_informacoes = html.Div(
    [
        html.Div(children = [
            html.Div(children =[
                dbc.Card(selic_anual),
            ],
            style = DIV_11_STYLE
            ),

            html.Div(children = [
                dbc.Card(inflacao_trimestrais_gps),
            ],
            style = DIV_12_STYLE
            ),
        ],
        ),

        html.Div(children = [
            html.Div(children = [
                dbc.Card(ipca_grupos_anuais),
            ],
            style = DIV_21_STYLE
            ),

            html.Div(children = [
                dbc.Card(inflacao_anuais_ipca_igpm),
            ],
            style = DIV_22_STYLE
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



