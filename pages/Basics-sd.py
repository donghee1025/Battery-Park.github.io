import os
import numpy as np
import dash
import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import dash_mantine_components as dmc
from collections import OrderedDict
from dash.exceptions import PreventUpdate

dash.register_page(
    __name__, name="basics", top_nav=True, path="/basics-sd"
    )

#dash.register_page(__name__, name="basics", top_nav=False)

data_election = OrderedDict(
    [
        (
            "Cell component",
            [
                "Electrodes",
                "Current collectors",
                "Separator",
                "Electrolyte",
                "Tabs",
            ], 
        ),
        (
            "Energy Cell",
            [
                "High coating density & thickness \n High active material loading percentage \n Low porosity", 
                "Thinner - Improved adhesion", 
                "Thin",
                "High ionic conductivity",
                "Thin/Narrow/A few tabs on each electrode (weight consideration)",         
            ],
        ),
        (
            "Power Cell", 
            [
                "Low coating density & thickness \n Low active material loading percentage \n High porosity", 
                "Thicker - Lower resistance", 
                "Thin",
                "High ionic conductivity",
                "Thick/Wide/Multiple tabs on each electrode (smoother ion transport)",      
            ]
        ),
    ],
)

dt = pd.DataFrame(data_election)


layout = html.Div([
             dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dcc.Markdown('* N/P Ratio', style={'font-size':'25px', 'textAlign':'left','font-weight':'bold'}),
                        dbc.Col([
                         html.Div('- By setting the ratio between the areal capacity of the anode and cathode for the different cycle rates, cell performance can be optimized. Typically, anodes are designed in a way to both have a higher areal capacity and a larger geometry/dimension than those of the cathode to lessen lithium metal plating and avoid high current density on the edge and thus the overlap effect (i.e. lithium plating). N/P ratio of 1-1.2 is commonly used in literature.', 
                                  style={'textAlign':'justify', 'margin-left':'20px', 'font-size':'18px'}),
                      ], width={"size": 7},
                         xs=12, sm=10, md=10, lg=7, xl=7
                         ), 
                        dbc.Col([
                        ], width={"size": 4},
                        xs=8, sm=8, md=6, lg=3, xl=3
                        ),
                    ],),
                    html.Br(),
                    dmc.Divider(size="md", color="grey"),
                    html.Br(),                   
                    dbc.Row([

                        dcc.Markdown('* Cell connection layout (mS-nP)', style={'font-size':'25px', 'textAlign':'left','font-weight':'bold'}),
                        dbc.Col([
                         html.Div('- For high-voltage packs, cells are connected in series to form a series-connected module (SCM).', style={'textAlign':'justify', 'margin-left':'20px', 'font-size':'18px'}),
                         dcc.Markdown(dangerously_allow_html=True, mathjax=True, children=("$$v_{pack}=m_{series}*v_{cell}$$"), style={'text-align':'center','font-size':'120%'}),
                         html.Div('- For high-current packs, cells are connected in parallel to form a parallel-connected module (PCM). Capacity scales with the number of cells in parallel.', style={'textAlign':'justify', 'margin-left':'20px', 'font-size':'18px'}),
                         dcc.Markdown(dangerously_allow_html=True, mathjax=True, children=("$$i_{pack}=n_{parallel}*i_{cell}$$"), style={'text-align':'center','font-size':'120%'}),
                         html.Div('- Total internal resistance of the pack can be estimated from the cell assuming the same open-circuit voltage and internal resistance:', style={'textAlign':'justify', 'margin-left':'20px', 'font-size':'18px'}),
                         dcc.Markdown(dangerously_allow_html=True, mathjax=True, children=("$$R_{pack}=\\frac{m_{series}}{n_{parallel}}*R_{cell}$$"), style={'text-align':'center','font-size':'120%'}),
                         html.Div('- Total pack energy and power can also be calculated:', style={'textAlign':'justify', 'margin-left':'20px', 'font-size':'18px'}),
                         dcc.Markdown(dangerously_allow_html=True, mathjax=True, children=("$$E_{pack}=m_{series}*n_{parallel}*Q_{cell}*v_{cell}$$"), style={'text-align':'center','font-size':'120%'}),
                         dcc.Markdown(dangerously_allow_html=True, mathjax=True, children=("$$P_{pack}=m_{series}*n_{parallel}*i_{cell}*v_{cell}$$"), style={'text-align':'center','font-size':'120%'}),
                         ], width={"size": 7},
                         xs=12, sm=10, md=10, lg=7, xl=7
                         ), 
                        dbc.Col([
                        html.Div( html.Img(src='https://dl.dropboxusercontent.com/scl/fi/jg6c9nt6e178rvwqgzmn1/Cell-in-Series-and-Parallel.png?rlkey=jx3kgx1r043llbnv0ewrfiykh&raw=1', style={"width":"140%"}), 
                                 ),
                        ], width={"size": 4},
                        xs=8, sm=8, md=6, lg=3, xl=3
                        ),
                    ],),
                    html.Br(),
                    dmc.Divider(size="md", color="grey"),
                    html.Br(),
                    dbc.Row([
                        dcc.Markdown('* Designing cell: Energy density vs Power capability?', style={'font-size':'25px', 'textAlign':'left','font-weight':'bold'}),
                        dbc.Col([
                        html.Div('- When designing the cell, the trade-off between energy density and power capability needs to be considered as both cannot go hand in hand. To increase the cell energy density, thicker and denser coating (i.e. higher material loading density) is needed for each electrode layer to store more energy. However, increasing the loading can engender many issues that raise the cell’s internal resistance including concentration polarization and uneven thermal distribution with possible ohmic heating. That is because low porosity, high tortuosity, and high thickness all translate to longer diffusion length of Li ions and possible bottleneck for Li flow in and out the cell. Hence power, which is the measure of how fast the energy can be driven in and out the electrode, is inevitably low for these cells.', style={'textAlign':'justify', 'margin-left':'20px','font-size':'18px'}),
                        html.Br(),
                        dash_table.DataTable(
                                style_cell={'font-family': 'Arial', 'font-size': '15px', 'text-align':'center', 'minWidth': '160px', 'width': '160px', 'maxWidth': '160px', 'margin-top':'10px', 'padding':2}, 
                                markdown_options={"html": True},
                                style_table={'overflowX': 'auto'},
                                style_data={
                                        'whiteSpace': 'normal',
                                        'color': 'black',
                                        'backgroundColor': 'white',
                                        'height':'auto',
                                        'lineheight':'5px',
                                },
                                style_data_conditional=[
                                {
                                    'if': {'column_id': 'Cell component'},
                                    'fontWeight': 'bold',
                                },
                                ],
                                style_header={
                                    'whiteSpace': 'normal',
                                    #'backgroundColor': 'rgb(210, 210, 210)',
                                    'backgroundColor': 'black',
                                    'color': 'white',
                                    'fontWeight': 'bold',
                                    'font-size': '16px',
                                    'text-align':'center',
                                },
                                data=dt.to_dict('records'),
                                columns=[{'id': c, 'name': c,"presentation": "markdown"} for c in dt.columns],
                        ),
                        ], width={"size": 7}, style={"margin-right":"10px"},
                       xs=12, sm=10, md=10, lg=8, xl=7
                       ), 
                        dbc.Col([
                        html.Div( html.Img(src='https://dl.dropboxusercontent.com/scl/fi/17gyxolvyjlaws7ksxw1m/power-vs-energy.png?rlkey=bikeko9bn4y6vehbhjv7aox8e&st=92q02hgo&raw=1', style={"width":"100%"}), 
                                 ),
                        ], width={"size": 4},
                        xs=8, sm=8, md=8, lg=5, xl=4
                        ),
                    ],),
                    html.Br(),
                    html.Br(),
                    dmc.Divider(size="md", color="grey"),
                    html.Br(),
                    dcc.Markdown(('* Reference'), style={'textAlign':'justify', 'margin-left':'0px', 'font-size':'20px', 'font-weight':'bold'}),
                   dcc.Markdown(('Michael J. Lain, et al., "Design Strategies for High Power vs. High Energy Lithium Ion Cells", _**batteries**_, 5, 64 (2019)'), style={'textAlign':'justify', 'margin-left':'0px', 'font-size':'18px'}),
                ],),
             ],
             style={'textAlign':'justify', 'margin-left':'30px', 'margin-right':'30px'},
             ),
             html.Div(id='Options-content'),
    ])