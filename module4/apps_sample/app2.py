## Evolving from the basics

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.title = 'NYC Wi-Fi Hotspots'

# API keys and datasets
map_data = pd.read_csv("nyc-wi-fi-hotspot-locations.csv")

# Selecting only required columns
map_data = map_data[["Borough", "Type", "Provider", "Name", "Location", "Latitude", "Longitude"]].drop_duplicates()

#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'



app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Maps and Tables',
                        className='nine columns'),
                html.Img(
                    src="https://www.fulcrumanalytics.com/wp-content/uploads/2017/12/cropped-site-logo-1.png",
                    className='three columns',
                    style={
                        'height': '16%',
                        'width': '16%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 12,
                        'padding-right': 0
                    },
                ),
                html.Div(children='''
                        Dash Tutorial video 04: Working with tables and maps.
                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Borroughs:'),
                        dcc.Checklist(
                                id = 'boroughs',
                                options=[
                                    {'label': 'Manhattan', 'value': 'MN'},
                                    {'label': 'Bronx', 'value': 'BX'},
                                    {'label': 'Queens', 'value': 'QU'},
                                    {'label': 'Brooklyn', 'value': 'BK'},
                                    {'label': 'Staten Island', 'value': 'SI'}
                                ],
                                value=['MN', 'BX', "QU",  'BK', 'SI'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Type:'),
                        dcc.Dropdown(
                            id='type',
                            options= [{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(map_data['Type'])],
                            multi=True,
                            value=list(set(map_data['Type']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
            ],
            className='row'
        ),

        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dt.DataTable(
                            rows=map_data.to_dict('records'),
                            columns=map_data.columns,
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            selected_row_indices=[],
                            id='datatable'),
                    ],
                    style = layout_table,
                    className="six columns"
                ),
                html.Div([
                        dcc.Graph(
                            id='bar-graph'
                        )
                    ], className= 'twelve columns'
                    ),
                html.Div(
                    [
                        html.P('Developed by Adriano M. Yoshino - ', style = {'display': 'inline'}),
                        html.A('amyoshino@nyu.edu', href = 'mailto:amyoshino@nyu.edu')
                    ], className = "twelve columns",
                       style = {'fontSize': 18, 'padding-top': 20}
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one'))



@app.callback(
    Output('datatable', 'rows'),
    [Input('type', 'value'),
     Input('boroughs', 'value')])
def update_selected_row_indices(type, borough):
    map_aux = map_data.copy()

    # Type filter
    map_aux = map_aux[map_aux['Type'].isin(type)]
    # Boroughs filter
    map_aux = map_aux[map_aux["Borough"].isin(borough)]

    rows = map_aux.to_dict('records')
    return rows

@app.callback(
    Output('bar-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)

    layout = go.Layout(
        bargap=0.05,
        bargroupgap=0,
        barmode='group',
        showlegend=False,
        dragmode="select",
        xaxis=dict(
            showgrid=False,
            nticks=50,
            fixedrange=False
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=False,
            fixedrange=False,
            rangemode='nonnegative',
            zeroline='hidden'
        )
    )

    data = Data([
         go.Bar(
             x=dff.groupby('Borough', as_index = False).count()['Borough'],
             y=dff.groupby('Borough', as_index = False).count()['Type']
         )
     ])

    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)