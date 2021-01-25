# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 21:41:56 2021

@author: Mara
"""
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

#key line to get the tab to render with a graph
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
assets=["eq","bo","mm","ci","de","cc","fc","gs","di","re"]
#assets_i=[s + "i" for s in assets]
lbls=["Equity", "Bonds", "Money Market", "Collective Investment", "Derivatives",
     "Commercial credit", "Financial Credit", "Guarantees", "Direct Investment", 
     "Real Estate"]

#dict(zip(lbls, assets))

# df2 = df.groupby([ 'Year', 'incomesubgroup'])[['ka', 'kai','kao']].mean()
# df2.reset_index(inplace=True)
# print(df2[:5])

# ------------------------------------------------------------------------------
# App layout
layout = html.Div(style={'width': "100%",
                             'backgroundColor': colors['background']},
                      children=[

    html.H1("Intensity of capital controls by asset classes",
            style={'text-align': 'center',
            'color': colors['text']}),

    dcc.Dropdown(id="slct_country2",
                 options=[{"label": x, "value":x} for x in df.Country.unique()],
                 multi=True,
                 value=["Algeria",""],
                 style={'width': "79%", 
                        'min-width':'450px',
                        'display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ),

 
    dcc.Dropdown(id="slct_flow2",
                 options=[{"label": "All", "value":""},
                          {"label": "Inflow", "value":"i"},
                          {"label": "Outflow", "value":"o"}],
                 value="",
                 multi=False,
                 style={'width': '20%',
                        'min-width':'100px',
                        'display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ),
    dcc.Slider(
        id='slct_year',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
        ),
     # dcc.Dropdown(id="slct_asset",
     #             options=[{"label": "Equity", "value":"eq"},
     #                      {"label": "Bonds", "value":"bo"},
     #                      {"label": "Direct Investment", "value":"di"},
     #                      {"label": "Money Market", "value": "mm"},
     #                      {"label": "Collective Investment", "value":"ci"},
     #                      {"label": "Derivatives", "value": "de"},
     #                      {"label": "Commercial credit", "value":"cc"},
     #                      {"label": "Financial credit", "value":"fc"},
     #                      {"label": "Real Estate", "value":"re"},
     #                      {"label": "Guarantees", "value": "gs"}],
     #             value="eq",
     #             multi=False,
     #             style={'width': "30%",'display': 'inline-block',
     #                    'backgroundColor': colors['background'], 
     #                    'color': colors['text']}
     #             ),
     
    html.Br(), 
    html.Div([
        dcc.Graph(id='capital_controls_assets_bar', figure={}),
    
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
    Output(component_id='capital_controls_assets_bar', component_property='figure'),
    Input(component_id='slct_country2', component_property='value'),
    Input(component_id='slct_flow2', component_property='value'),
    Input(component_id='slct_year', component_property='value')
)
def update_asset_bar(option_country, option_flow, option_year):
    print(option_country)
    print(option_flow)
    print(option_year)
    print(type(option_country))
    print(type(option_flow))

    #container = "The income group chosen by user was: {}".format(option_income)

    dff = df.copy()
    vv=[s+option_flow for s in assets]
    vv.append('Country')
    dff = dff.loc[(dff["Country"].isin(option_country))&(dff["Year"] == option_year),vv]        
    l2=lbls.copy()
    l2.append('Country')
    dff.columns=l2
    #dff = dff[(dff["Country"]==option_country) & (dff["Year"] == option_year)]
    #r=dff[[s+option_flow for s in assets]].values.tolist()[0]
    #r=dff[[s+option_flow for s in assets]]
    print(dff)
    dff=pd.melt(dff, id_vars='Country')
                 
     # Plotly Express
    fig = px.bar(dff, y='value', x='variable', 
                 labels={'variable':"", 'value':"Intensity of restrictions"},
                 template='simple_white',
                 color="Country", barmode="group")

    return fig


# ------------------------------------------------------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True)