# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools
import plotly.figure_factory as ff



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#select distinct boronames
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=distinct(boroname)')
boroughs = pd.read_json(soql_url).sort_values(['boroname_1'], ascending=[True])

#select distinct species

soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=distinct(spc_common)')
spc_common = pd.read_json(soql_url).sort_values(['spc_common_1'], ascending=[True])

alltree_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=*' +\
        '&$where=steward is not null and health  is not null').replace(' ', '%20')

trees = pd.read_json(alltree_url)
trees['BiVariateCatg'] = trees['steward'].astype(str) + '|' +  trees['health'].astype(str)
trees['BiVariateCatg'] = pd.Categorical(trees['BiVariateCatg'])
import datashader as ds
import datashader.transfer_functions as tf
import datashader.glyphs
from datashader import reductions
from datashader.core import bypixel
from datashader.utils import lnglat_to_meters as webm, export_image
from datashader.colors import colormap_select, Greys9, viridis, inferno
from functools import partial
#Defining some helper functions for DataShader
background = "black"
export = partial(export_image, background = background, export_path="export")
cm = partial(colormap_select, reverse=(background!="black"))


colorscale_seq = {'None|Poor' : "#543005", 'None|Good' : "#8c510a", 'None|Fair' : "#bf812d",
              '1or2|Poor' : "#dfc27d", '1or2|Good' : "#f6e8c3", '1or2|Fair' : "#f5f5f5", 
              '3or4|Poor' :"#c7eae5",'3or4|Good' : "#c7eae5", '3or4|Fair': "#80cdc1", 
              '4orMore|Poor' : "#35978f",'4orMore|Good' : "#01665e", '4orMore|Fair' : "#003c30"
             }

colorscale_df = {'None|Poor' : "#2ca25f", 'None|Good' : "#e5f5f9", 'None|Fair' : "#99d8c9",
              '1or2|Poor' : "#b3cde3", '1or2|Good' : "#fdcc8a", '1or2|Fair' : "#CBD2AA", 
              '3or4|Poor' :"#8c96c6",'3or4|Good' : "#C5B1A8", '3or4|Fair': "#fc8d59", 
              '4orMore|Poor' : "#88419d",'4orMore|Good' : "#FDCC8A", '4orMore|Fair' : "#d7301f"
             }




#['#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3','#f5f5f5','#c7eae5','#80cdc1','#35978f','#01665e','#003c30']
NewYorkCity   = (( -74.29,  -73.69), (40.49, 40.92))
cvs = ds.Canvas(1000, 1000, *NewYorkCity)
ds.count_cat('BiVariateCatg')
agg = cvs.points(trees, 'longitude', 'latitude', ds.count_cat('BiVariateCatg'))
view = tf.shade(agg, color_key = colorscale_df)
img = export(tf.spread(view, px=1), 'choropleth')

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='New York City tree census - 2015',
                        className='nine columns')
            ], className="row"
        ),
            
    html.Div(
            [
                html.H3(children='Species Health Proportions',
                        className='nine columns')
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.H6('Choose Borroughs:'),
                        dcc.Checklist(
                                id = 'boroughs',
                                options=[{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(boroughs['boroname_1'])],
                                value=list(set(boroughs['boroname_1']))[0:4],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.H6('Species:'),
                        dcc.Dropdown(
                            id='species',
                            options=[{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(spc_common['spc_common_1'])],
							value=list(set(spc_common['spc_common_1']))[0:2],
                            multi=True
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
                html.Div([
                        dcc.Graph(
                            id='bar-graph'
                        )
                    ], className= 'twelve columns'
                    )
            ], className="row"
        ),
        
        html.Div(
            [   
                html.H3(children='Correlation between Health V/S Steward activities',
                        className='nine columns'),
                html.Img(
                src="ny_choropleth.png",
                className='nine columns',
            ),
            ], className="row"
        )
                        
        
    ], className='ten columns offset-by-one'))


#export(tf.spread(view, px=1), 'choropleth')



def format(itemlist):
    #i/p List  ["Bronx", "Queens" ]
    #o/p String : ("Bronx", "Queens")
    tmpList = ['\"' + str(elm) + '\"' for elm in itemlist]
    return '(' + ', ' .join(tmpList) + ')'

@app.callback(
    Output('bar-graph', 'figure'),
    [Input('boroughs', 'value'),
     Input('species', 'value')])
def update_figure(boroughs, species):

    soql_url = ''
    if ((len(boroughs)>0) & (len(species) > 0)):
        soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
                    '$select=health , spc_common ,boroname ,count(tree_id)' +\
                    '&$where=boroname in ' + format(boroughs) + ' and spc_common in ' + format(species) + ' ' +\
                    '&$group=health,spc_common,boroname').replace(' ', '%20')
    else:
        return go.Figure(data=[])

    
    
    soql_trees = pd.read_json(soql_url)
    soql_trees['boroname_and_species'] = soql_trees['boroname'] + ',' + soql_trees['spc_common']
    soql_trees = soql_trees.drop(columns=['spc_common', 'boroname'])
    soql_trees['health_ratio'] = soql_trees.groupby(['boroname_and_species'])['count_tree_id'].transform(lambda x: x/x.sum()*100)
    soql_trees = soql_trees.sort_values(['boroname_and_species'], ascending=[True])


    df_good =soql_trees[soql_trees['health'] == 'Good']
    df_fair =soql_trees[soql_trees['health'] == 'Fair']
    df_poor =soql_trees[soql_trees['health'] == 'Poor']

    fig = go.Figure(data=[
                go.Bar(name='Good', x=df_good['boroname_and_species'], y=df_good['health_ratio']),
                go.Bar(name='Fair', x=df_fair['boroname_and_species'], y=df_fair['health_ratio']),
                go.Bar(name='Poor', x=df_poor['boroname_and_species'], y=df_poor['health_ratio'])
                ])
                # Change the bar mode
    fig.update_layout(barmode='group')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
	