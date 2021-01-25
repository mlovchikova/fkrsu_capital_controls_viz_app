# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:51:00 2021

@author: Mara
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from fksru_capital_controls import app
from apps import gr1, gr2, gr3

app.layout = html.Div([
    dcc.Tabs(id='tabs-capital_controls', value='tab1', children=[
        dcc.Tab(gr1.layout, label='By income group'),
        dcc.Tab(gr2.layout, label='By asset classes'),
        dcc.Tab(gr3.layout, label='Across asset classes'),
    ]),   
])



if __name__ == '__main__':
    app.run_server(debug=True)