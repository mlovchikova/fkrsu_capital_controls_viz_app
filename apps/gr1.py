# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:48:48 2021

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

#key line
from fksru_capital_controls import app
colors = {
    'background': '#FDFFFF',
    'text': '#1995AD'
}
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("FKRSU_Update_Jun_13_2019-utf.csv")
df=df.replace(['n.a'], '')

df2 = df.groupby([ 'Year', 'incomesubgroup'])[['ka', 'kai','kao']].mean()
df2.reset_index(inplace=True)
print(df2[:5])

# ------------------------------------------------------------------------------
# App layout
layout = html.Div(style={'width': "100%",'backgroundColor': colors['background']},
                      children=[

    html.H1("Intensity of capital controls",
            style={'text-align': 'center',
            'color': colors['text']}),

    dcc.Dropdown(id="slct_incomegroup",
                 options=[{"label": x, "value":x} for x in df2.incomesubgroup.unique()],
                 multi=True,
                 value=["Low income", ""],
                 style={'width': "50%",
                        'min-width': '350px', 'display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ),
    dcc.Dropdown(id="slct_flow_agg",
                 options=[{"label": "All", "value":"ka"},
                          {"label": "Inflow", "value":"kai"},
                          {"label": "Outflow", "value":"kao"}],
                 value="ka",
                 multi=False,
                 style={'width': "40%",
                        'min-width':'100px','display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ), 
    
    html.Br(),
    html.Div([
        dcc.Graph(id='capital_controls_agg', figure={}),
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
        
        For more details visit [http://www.columbia.edu/~mu2166/fkrsu/](/)
        
        _Source_: Fernandez, Andres, Michael Klein, Alessandro Rebucci,
        Martin Schindler, and Martin Uribe, 
        'Capital Control Measures: A New Dataset,'
        IMF Economic Review 64, 2016, 548-574
    
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
    Output(component_id='capital_controls_agg', component_property='figure'),
    Input(component_id='slct_incomegroup', component_property='value'),
    Input(component_id='slct_flow_agg', component_property='value')
)
def update_income_line(option_income, option_flow):
   
    
    dff = df2.copy()
    dff = dff[dff["incomesubgroup"].isin(option_income)]
      # Plotly Express
    fig = px.line(
        data_frame=dff,
        x='Year',
        y=option_flow,
        color='incomesubgroup',
        labels={option_flow: 'Intensity of capital controls', 'Year':''},
        template='simple_white'
        )
    
    fig.update_layout(
       font_color=colors['text']
    )
    fig.update_xaxes(showline=True, mirror=True,
                      linecolor=colors['text']
                      )
    fig.update_yaxes(showline=True, mirror=True,
                      linecolor=colors['text']
                      )
   
    return fig
   

# for a tab no need for the following:
# ------------------------------------------------------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True)