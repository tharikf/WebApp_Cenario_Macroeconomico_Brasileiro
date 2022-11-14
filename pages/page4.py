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
    'top' : 520,
    'left' : 288,
    'bottom' : 0,
    'width' : '54rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

DIV_22_STYLE = {
    'position' : 'fixed',
    'top' : 520,
    'left' : 1085,
    'bottom' : 0,
    'width' : '54rem',
    'background-color' : '#FFFFFF',
    'display' : 'inline-block',
}

# Informacoes #
expec = Expectativas()
entidade_anuais = 'ExpectativasMercadoAnuais'
def obtendo_expectativas(indicador, entidade, respondentes):
    
    # Filtrando para previsoes dos ultimos 3 meses
    tres_meses = datetime.date.today() - datetime.timedelta(days = 90)
    tres_meses = tres_meses.strftime('%Y-%m-%d')
    
    # Obtendo dados
    ep = expec.get_endpoint(entidade)
    df_ep = ep.query().filter(ep.Indicador == indicador,
                              ep.Data >= tres_meses,
                              ep.numeroRespondentes >= respondentes).select(ep.Data, ep.DataReferencia,
                                                           ep.Media, ep.Minimo, ep.Maximo,
                                                           ep.Indicador).collect()

    return df_ep

# Divida Bruta do Governo #
div_bruta_total = obtendo_expectativas('Dívida bruta do governo geral', entidade_anuais, 10)

def unindo_gov(x):
    
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
    df.columns = ['metrica_ano', 'valor']
    df[['metrica', 'anos']] = df['metrica_ano'].str.split('_', n = 1, expand = True)
    df = df.drop(columns = 'metrica_ano')
    df = df[['anos', 'metrica', 'valor']]
    df.columns = ['Anos', 'Métrica', 'Valor']
    df['Valor'] = round(df['Valor'], 2)
    df['Métrica'] = np.where(df['Métrica'] == 'maximo', 'Máximo',
                              np.where(df['Métrica'] == 'media', 'Média', 'Mínimo'))
    
    return df

div_bruta_df = unindo_gov(div_bruta_total)

fig_div_bruta = px.bar(div_bruta_df, x = 'Anos', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_div_bruta.update_layout(title = '<br><sup>Valores em Porcentagem do PIB</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(tick0 = 0, dtick = 10))
fig_div_bruta.update_yaxes(range = (0, 100), constrain = 'domain', ticksuffix = '%')
# Finalizando Divida Bruta do Governo #

# Dívida Líquida do Governo #
div_liquida_total = obtendo_expectativas('Dívida líquida do setor público', entidade_anuais, 10)
div_liquida_df = unindo_gov(div_liquida_total)

fig_div_liquida = px.bar(div_liquida_df, x = 'Anos', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_div_liquida.update_layout(title = '<br><sup>Valores em Porcentagem do PIB</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(tick0 = 0, dtick = 10))
fig_div_liquida.update_yaxes(range = (0, 100), constrain = 'domain', ticksuffix = '%')
# Finalizando Dívida Líquida do Governo #

# Resultado Primario #
primario_total = obtendo_expectativas('Resultado primário', entidade_anuais, 10)
primario_df = unindo_gov(primario_total)

fig_primario = px.bar(primario_df, x = 'Anos', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_primario.update_layout(title = '<br><sup>Valores em Porcentagem do PIB</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(dtick = 0.3))

fig_primario.update_yaxes(range = (-1.5, 1.5), constrain = 'domain', ticksuffix = '%')
# Finalizado Resultado Primario #

# Resultado Nominal #
nominal_total = obtendo_expectativas('Resultado nominal', entidade_anuais, 10)
nominal_df = unindo_gov(nominal_total)

fig_nominal = px.bar(nominal_df, x = 'Anos', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_nominal.update_layout(title = '<br><sup>Valores em Porcentagem do PIB</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(dtick = 1))

fig_nominal.update_yaxes(range = (-10, 0), constrain = 'domain', ticksuffix = '%')
# Finalizado Resultado Nominal #

# Investimento Direto no Pais #
invest_total = obtendo_expectativas('Investimento direto no país', entidade_anuais, 10)
invest_total_df = unindo_gov(invest_total)

fig_invest = px.bar(invest_total_df, x = 'Anos', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_invest.update_layout(title = '<br><sup>Valores em Bilhões</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas', yaxis = dict(tick0 = 0, dtick = 10))
fig_invest.update_yaxes(range = (0, 100), constrain = 'domain', tickprefix = 'R$')
# Finalizado Investimento Direto no Pais #

# Conta Corrente #
conta_corrente = obtendo_expectativas('Conta corrente', entidade_anuais, 10)
conta_corrente_df = unindo_gov(conta_corrente)

fig_conta = px.bar(conta_corrente_df, x = 'Anos', y = 'Valor', color = 'Métrica', barmode = 'group',
                        color_discrete_sequence = ['#560699', '#080699', '#E41006'], template = 'plotly_white')

fig_conta.update_layout(title = '<br><sup>Valores em Bilhões</sup>', title_x = 0.0, xaxis_title = '', yaxis_title = '',
                           legend_title = 'Métricas')

fig_conta.update_yaxes(range = (-60, 0), constrain = 'domain', tickprefix = 'R$')
# Finalizado Conta Corrente #

# Plot das Informacoes
divida_governo = [
    dbc.CardHeader('Previsões para a Dívida do Governo'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'div-bruta',
                                figure = fig_div_bruta,
                                style = {'height' : 360, 'width' : 700}),
        ), label = 'Dívida Bruta do Governo'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'div-liquida',
                                figure = fig_div_liquida,
                                style = {'height' : 360, 'width' : 700}),
        ), label = 'Dívida Líquida do Setor Público'
            ),
        ]
    )
]

resultado_governo = [
    dbc.CardHeader('Previsões para o Resultado Primário e Nominal'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'resul-prim',
                                figure = fig_primario,
                                style = {'height' : 360, 'width' : 700}),
        ), label = 'Resultado Primário do Governo'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'resul-nom',
                                figure = fig_nominal,
                                style = {'height' : 360, 'width' : 700}),
        ), label = 'Resultado Nominal do Governo'
            ),
        ]
    )
]

invest_direto = [
    dbc.CardHeader('Previsões do Investimento Direto no País'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'invest-prev',
                        figure = fig_invest,
                        style = {'height' : 360, 'width' : 750}),
        ],
    ),
]

conta_corr = [
    dbc.CardHeader('Previsões da Conta Corrente do País'),
    dbc.CardBody(
        [
            dcc.Graph(id = 'conta-prev',
                        figure = fig_conta,
                        style = {'height' : 360, 'width' : 750}),
        ],
    ),
]

area_informacoes = html.Div(
    [
        html.Div(children = [
            html.Div(children =[
                dbc.Card(divida_governo),
            ],
            style = DIV_11_STYLE
            ),

            html.Div(children = [
                dbc.Card(resultado_governo),
            ],
            style = DIV_12_STYLE
            ),
        ],
        ),

        html.Div(children = [
            html.Div(children = [
                dbc.Card(invest_direto),
            ],
            style = DIV_21_STYLE
            ),

            html.Div(children = [
                dbc.Card(conta_corr),
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

