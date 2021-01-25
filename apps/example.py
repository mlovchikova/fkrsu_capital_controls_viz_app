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

assets=["eq","bo","mm","ci","de","cc","fc","gs","di","re"]
#assets_i=[s + "i" for s in assets]
lbls=["Equity", "Bonds", "Money Market", "Collective Investment", "Derivatives",
     "Commercial credit", "Financial Credit", "Guarantees", "Direct Investment", 
     "Real Estate"]

#------------------------------------------------------------------------
app.layout = html.Div([
    html.Div([

        html.Div([
            html.P(),
            #start left title and dropdown menus
            html.H1("Intesity of capital controls",
            style={'text-align': 'center',
            'color': colors['text']}
            ),

            dcc.Dropdown(id="slct_country",
                 options=[{"label": x, "value":x} for x in df.Country.unique()],
                 multi=True,
                 value=["Algeria",""],
                 style={'display': 'inline-block', 
                        'width': '79%',
                        'min-width':'450px',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ),
            dcc.Dropdown(id="slct_flow",
                 options=[{"label": "All", "value":"ka"},
                          {"label": "Inflow", "value":"kai"},
                          {"label": "Outflow", "value":"kao"}],
                 value="ka",
                 multi=False,
                 style={'display': 'inline-block',
                        'width': '20%',
                        'min-width':'100px',
                        'resize': 'horizontal',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 )
        ],
        style={'width': '49%', 'display': 'inline-block',
               #'resize': 'vertical',
               }),

        html.Div([
            html.H1("Intensity of capital controls by asset classes",
            style={'text-align': 'center',
            'color': colors['text']}),

  
            dcc.Slider(
                id='slct_year',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(year): str(year) for year in df['Year'].unique()},
                step=None
                ),
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
            ], style={
                'padding': '5px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='capital_controls_ts', figure={}
        )
    ], style={'width': '49%', 'display': 'inline-block',
              'padding': '5 5'}),
    html.Div([
        dcc.Graph(
            id='capital_controls_assets_bar'
            )
        #dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div([
        dcc.Dropdown(id="slct_incomegroup",
                 options=[{"label": x, "value":x} for x in df2.incomesubgroup.unique()],
                 multi=False,
                 value="Low income",
                 style={'width': "50%", 'display': 'inline-block',
                        'backgroundColor': colors['background'], 
                        'color': colors['text']}
                 ),
    
        html.Br(),

        dcc.Graph(id='capital_controls_agg', figure={}),
        ], 
        style={'width': '49%', 'display': 'inline-block',
              'padding': '5 5'}),


    html.Div(id='output_container', 
              style={'backgroundColor': colors['background'], 
                    'color': colors['text'], 'font_size':8},
              children=[])
    
])

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
    #container="Source: Fernandez, Andres, Michael Klein, Alessandro Rebucci, Martin Schindler, and Martin Uribe, 'Capital Control Measures: A New Dataset,' IMF Economic Review 64, 2016, 548-574. Intensity of capital controls is averaged across all countries in {} group".format(option_income)
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
    return fig              

@app.callback(
    Output(component_id='capital_controls_assets_bar', component_property='figure'),
    Input(component_id='slct_country', component_property='value'),
    Input(component_id='slct_flow', component_property='value'),
    Input(component_id='slct_year', component_property='value')
)
def update_asset_bar(option_country, option_flow, option_year):
    if option_flow=='ka':
            flow=""
    elif option_flow=='kai':
            flow='i'
    else:
        flow='o'        
    print(option_country)
    print(option_flow)
    print(option_year)
    print(type(option_country))
    print(type(option_flow))

    
    dff = df.copy()
    vv=[s+flow for s in assets]
    vv.append('Country')
    dff = dff.loc[(dff["Country"].isin(option_country))&(dff["Year"] == option_year),vv]        
    l2=lbls.copy()
    l2.append('Country')
    dff.columns=l2
    print(dff)
    dff=pd.melt(dff, id_vars='Country')
                 
    #container="Source: Fernandez, Andres, Michael Klein, Alessandro Rebucci, Martin Schindler, and Martin Uribe, 'Capital Control Measures: A New Dataset,' IMF Economic Review 64, 2016, 548-574. Intensity of capital controls is averaged across asset classes".format()
    # Plotly Express
    fig = px.bar(dff, y='value', x='variable', 
                 labels={'variable':"", 'value':"Intensity of restrictions"},
                 template='simple_white',
                 color="Country", barmode="group")
    

    return fig


@app.callback(
    Output(component_id='capital_controls_ts', component_property='figure'),
    Output(component_id='output_container', component_property='children'),
    Input(component_id='slct_country', component_property='value'),
    Input(component_id='slct_flow', component_property='value')
)
def update_graph(option_country, option_flow):
    print(option_country)
    print(option_flow)
    print(type(option_country))
    print(type(option_flow))

    #container = "The income group chosen by user was: {}".format(option_income)

    dff = df.copy()
    option_country=list(option_country)
        
    dff = dff[dff["Country"].isin(option_country)]
   
    #dff = dff[dff["Year"] == "2017"]
    container="Source: Fernandez, Andres, Michael Klein, Alessandro Rebucci, Martin Schindler, and Martin Uribe, 'Capital Control Measures: A New Dataset,' IMF Economic Review 64, 2016, 548-574. Intensity of capital controls is averaged across asset classes".format()
    # Plotly Express
    fig = px.line(
        data_frame=dff,
        x='Year',
        y=option_flow,
        color='Country',
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
    
    return fig, container

#-----------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)