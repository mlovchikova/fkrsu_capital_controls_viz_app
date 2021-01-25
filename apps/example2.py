# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:48:48 2021

@author: Mara
"""


import pandas as pd
import geopandas as gpd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

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
app.layout = html.Div(style={'width': "50%",'backgroundColor': colors['background']},
                      children=[

    html.H1("Intesity of capital controls",
            style={'text-align': 'center',
            'color': colors['text']}),

    dcc.Dropdown(id="slct_incomegroup",
                 options=[{"label": x, "value":x} for x in df2.incomesubgroup.unique()],
                 multi=False,
                 value="Low income",
                 style={'width': "50%", 'display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ),
    dcc.Dropdown(id="slct_flow",
                 options=[{"label": "All", "value":"ka"},
                          {"label": "Inflow", "value":"kai"},
                          {"label": "Outflow", "value":"kao"}],
                 value="ka",
                 multi=False,
                 style={'width': "40%",'display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ), 
    
    html.Br(),

    dcc.Graph(id='capital_controls_agg', figure={}),
    
     html.Div(id='output_container', 
              style={'width':'70%','backgroundColor': colors['background'], 
                    'color': colors['text'], 'font_size':6},
              children=[])
 
    

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='capital_controls_agg', component_property='figure'),
    Input(component_id='slct_incomegroup', component_property='value'),
    Input(component_id='slct_flow', component_property='value')
)
def update_graph(option_income, option_flow):
    print(option_income)
    print(option_flow)
    print(type(option_income))
    print(type(option_flow))

    #container = "The income group chosen by user was: {}".format(option_income)

    dff = df2.copy()
    dff = dff[dff["incomesubgroup"] == option_income]
    #dff = dff[dff["Year"] == "2017"]
    container="Source: Fernandez, Andres, Michael Klein, Alessandro Rebucci, Martin Schindler, and Martin Uribe, 'Capital Control Measures: A New Dataset,' IMF Economic Review 64, 2016, 548-574. Intensity of capital controls is averaged across all countries in {} group".format(option_income)
    # Plotly Express
    fig = px.line(
        data_frame=dff,
        x='Year',
        y=option_flow,
        labels={option_flow: 'Intensity of capital controls', 'Year':''},
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
    return fig,container
    


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)