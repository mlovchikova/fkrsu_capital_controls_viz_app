# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 20:34:06 2021

@author: Mara
"""

import pandas as pd
#import geopandas as gpd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#key line to get figures to render
from fksru_capital_controls import app
colors = {
    'background': '#FDFFFF',
    'text': '#1995AD'
}
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("FKRSU_Update_Jun_13_2019-utf.csv")
df=df.replace(['n.a'], '')

print(df[:5])

# df2 = df.groupby([ 'Year', 'incomesubgroup'])[['ka', 'kai','kao']].mean()
# df2.reset_index(inplace=True)
# print(df2[:5])

# ------------------------------------------------------------------------------
# App layout
layout = html.Div(style={'width': "100%",
                             'backgroundColor': colors['background']},
                      children=[

    html.H1("Capital controls over time across asset classes and countries",
            style={'text-align': 'center',
            'color': colors['text']}),

    dcc.Dropdown(id="slct_country",
                 options=[{"label": x, "value":x} for x in df.Country.unique()],
                 multi=True,
                 value=["Algeria",""],
                 style={#'width': "40%", 
                        'min-width':'300px', 'display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ),
    dcc.Dropdown(id="slct_flow",
                 options=[{"label": "All", "value":""},
                          {"label": "Inflow", "value":"i"},
                          {"label": "Outflow", "value":"o"}],
                 value="",
                 multi=False,
                 #title="Select inflow, outflow or all",
                 style={#'width': '20%',
                        'min-width':'100px','display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ), 
    dcc.Dropdown(id="slct_asset",
                  options=[{"label": "Equity", "value":"eq"},
                           {"label": "Bonds", "value":"bo"},
                           {"label": "Direct Investment", "value":"di"},
                           {"label": "Money Market", "value": "mm"},
                           {"label": "Collective Investment", "value":"ci"},
                           {"label": "Derivatives", "value": "de"},
                           {"label": "Commercial credit", "value":"cc"},
                           {"label": "Financial credit", "value":"fc"},
                           {"label": "Real Estate", "value":"re"},
                           {"label": "Guarantees", "value": "gs"},
                           {"label":"All assets","value": "ka"}],
                  value="ka",
                  multi=False,
                  #title="Select an asset class",
                  style={#'width': "20%",
                         'min-width':'200px','display': 'inline-block',
                         'backgroundColor': colors['background'], 
                         'color': colors['text']}
                  ), 
    
    
    html.Div([
    dcc.Graph(id='capital_controls_ts', figure={}           
              ),
    ],
        style={'width': "69%",
                     'display': 'inline-block',}
    ),
    html.Div([
    dcc.Markdown(
        '''
        Intensity of capital controls is an index for each asset class
        and for each flow direction. Existence of de jure restriction is coded as 1,
        and the absence of such restriction is coded as 0. If asset class has
        subcategories by residence, then index is averaged across subcategories.
        
        For more detailes visit [http://www.columbia.edu/~mu2166/fkrsu/](/)
        
        Source: Fernandez, Andres, Michael Klein, Alessandro Rebucci, Martin Schindler, and Martin Uribe, 'Capital Control Measures: A New Dataset,' IMF Economic Review 64, 2016, 548-574
    
        '''
        ),
    
    ],
        style={'width': "25%",'display': 'inline-block',
               'vertical-align': 'top', "border-width":"0.5px",
               "border-color": colors['text'], "border-style":"solid", 
               "padding": "5px 5px 5px 5px",
                         'backgroundColor': colors['background'], 
                         'color': colors['text'],'font_size':10}
        ),
    

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='capital_controls_ts', component_property='figure'),
    Input(component_id='slct_country', component_property='value'),
    Input(component_id='slct_flow', component_property='value'),
    Input(component_id='slct_asset', component_property='value')
)
def update_asset_line(option_country, option_flow, option_asset):
    print(option_country)
    print(option_flow)
    print(type(option_country))
    print(type(option_flow))

    #container = "The income group chosen by user was: {}".format(option_income)

    dff = df.copy()
    option_country=list(option_country)
        
    dff = dff[dff["Country"].isin(option_country)]
   
    
    # Plotly Express
    fig = px.line(
        data_frame=dff,
        x='Year',
        y=option_asset+option_flow,
        color='Country',
        labels={option_asset+option_flow: 'Intensity of capital controls', 'Year':''},
        template='simple_white'
        )
    
    fig.update_layout(
    #plot_bgcolor=colors['background'],
    #paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
    fig.update_xaxes(showline=True, mirror=True,
                     linecolor=colors['text']
                     )
    fig.update_yaxes(showline=True, mirror=True,
                     linecolor=colors['text']
                     )
    # fig = px.choropleth(
    #     data_frame=dff,
    #     locationmode='USA-states',
    #     locations='state_code',
    #     scope="usa",
    #     color='Pct of Colonies Impacted',
    #     hover_data=['State', 'Pct of Colonies Impacted'],
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
    #     template='plotly_dark'
    # )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )
    #container, 
    return fig
    


# ------------------------------------------------------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True)