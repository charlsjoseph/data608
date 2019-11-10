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
import base64
import researchpy as rp
import plotly.graph_objects as go
from plotly.subplots import make_subplots

 



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

soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=*' +\
        '&$where=health  is not null &$limit=80000').replace(' ', '%20')
treesall = pd.read_json(soql_url)
trees_si = treesall[treesall['boroname'] == 'Staten Island']
trees_mn = treesall[treesall['boroname'] == 'Manhattan']
trees_qn = treesall[treesall['boroname'] == 'Queens']
trees_bx = treesall[treesall['boroname'] == 'Bronx']
trees_bk = treesall[treesall['boroname'] == 'Brooklyn']

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
        html.Div(
                    [
                        html.H6('Filter no stweard activities:'),
                        dcc.Checklist(id = 'stewardact',
                                      options=[{'label': 'Steward', 'value': 'N'}],
                                      value=['Y']
                                ),
                    ],
                    className='two columns',
                    style={'margin-top': '10'}
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
                html.Div([
                        dcc.Graph(
                            id='bar-chartb'
                        )
                    ], className= 'twelve columns'
                    )
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
@app.callback(
    Output('bar-chartb', 'figure'),
    [Input('stewardact', 'value')])
def update_figureb(stewardact):
   
   trees_mn_count = trees_mn.groupby(["steward", "health" ]).tree_id.agg(['count']).reset_index()
   trees_mn_sum = trees_mn_count.groupby(["steward"])['count'].agg(['sum'])
   df_merge_col = pd.merge(trees_mn_sum, trees_mn_count, on='steward', how='inner').sort_values(['steward'])
   df_merge_col['prop'] = df_merge_col.apply(lambda row: row['count']/row['sum'] *100, axis=1)
   #Queens
   trees_qn_count = trees_qn.groupby(["steward", "health" ]).tree_id.agg(['count']).reset_index()
   trees_qn_sum = trees_qn_count.groupby(["steward"])['count'].agg(['sum'])
   df_merge_qn = pd.merge(trees_qn_sum, trees_qn_count, on='steward', how='inner').sort_values(['steward'])
   df_merge_qn['prop'] = df_merge_qn.apply(lambda row: row['count']/row['sum'] *100, axis=1)
   #SI
   trees_si_count = trees_si.groupby(["steward", "health" ]).tree_id.agg(['count']).reset_index()
   trees_si_sum = trees_si_count.groupby(["steward"])['count'].agg(['sum'])
   df_merge_si = pd.merge(trees_si_sum, trees_si_count, on='steward', how='inner').sort_values(['steward'])
   df_merge_si['prop'] = df_merge_si.apply(lambda row: row['count']/row['sum'] *100, axis=1)
    #BX
   trees_bx_count = trees_bx.groupby(["steward", "health" ]).tree_id.agg(['count']).reset_index()
   trees_bx_sum = trees_bx_count.groupby(["steward"])['count'].agg(['sum'])
   df_merge_bx = pd.merge(trees_bx_sum, trees_bx_count, on='steward', how='inner').sort_values(['steward'])
   df_merge_bx['prop'] = df_merge_bx.apply(lambda row: row['count']/row['sum'] *100, axis=1)
    #BK
   trees_bk_count = trees_bk.groupby(["steward", "health" ]).tree_id.agg(['count']).reset_index()
   trees_bk_sum = trees_bk_count.groupby(["steward"])['count'].agg(['sum'])
   df_merge_bk = pd.merge(trees_bk_sum, trees_bk_count, on='steward', how='inner').sort_values(['steward'])
   df_merge_bk['prop'] = df_merge_bk.apply(lambda row: row['count']/row['sum'] *100, axis=1)
     
  #figure = go.Figure(data=[go.Bar(name='Poor', x=df_merge_col[df_merge_col['health']=='Poor']['steward'], y=df_merge_col[df_merge_col['health']=='Poor']['prop']),
                #go.Bar(name='Fair', x=df_merge_col[df_merge_col['health']=='Fair']['steward'], y=df_merge_col[df_merge_col['health']=='Fair']['prop']),
                #go.Bar(name='Good', x=df_merge_col[df_merge_col['health']=='Good']['steward'], y=df_merge_col[df_merge_col['health']=='Good']['prop'])
               # ])
                        
                        
   figure1 = make_subplots(rows=3, cols=2, 
                start_cell="bottom-left",
                subplot_titles=("Manhatten (p-value = 0.07)", "Queens (p-value = 0.001)" , "Staten Island (p-value = 0.001)", 
                                "Bronx" , "Brookyln"))
# row1 col2 Manhatten

   figure1.add_trace((
                   go.Bar(
                       marker_color='lightskyblue' , name='Poor', 
                       x=df_merge_col[df_merge_col['health']=='Poor']['steward'], 
                       y=df_merge_col[df_merge_col['health']=='Poor']['prop'])
                   ),row=1, col=1)
   figure1.add_trace((
                   go.Bar(
                           marker_color = 'palegreen' ,
                           name='Fair', 
                           x=df_merge_col[df_merge_col['health']=='Fair']['steward'], 
                           y=df_merge_col[df_merge_col['health']=='Fair']['prop'])
                   ),row=1, col=1)
   figure1.add_trace(( 
                   go.Bar( 
                           marker_color = 'lightsalmon' ,
                           name='Good', 
                           x=df_merge_col[df_merge_col['health']=='Good']['steward'], 
                           y=df_merge_col[df_merge_col['health']=='Good']['prop'])
                    )  ,row=1, col=1)
# row1 col2 Queens
   figure1.add_trace((
               go.Bar(
                       marker_color = 'lightskyblue' ,
                       name='Poor', 
                       showlegend = False,
                       x=df_merge_qn[df_merge_col['health']=='Poor']['steward'], 
                       y=df_merge_qn[df_merge_col['health']=='Poor']['prop'])
                   )  ,row=1, col=2)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'palegreen',
                   name='Fair', 
                   showlegend = False,
                   x=df_merge_qn[df_merge_col['health']=='Fair']['steward'], 
                   y=df_merge_qn[df_merge_col['health']=='Fair']['prop'])
               )  ,row=1, col=2)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'lightsalmon' ,
                   name='Good', 
                   showlegend = False,
                   x=df_merge_qn[df_merge_col['health']=='Good']['steward'], 
                   y=df_merge_qn[df_merge_col['health']=='Good']['prop'])
           )  ,row=1, col=2)

# row2 col1 Staten Island

   figure1.add_trace((
               go.Bar(
                       marker_color = 'lightskyblue' ,
                       name='Poor', 
                       showlegend = False,
                       x=df_merge_si[df_merge_si['health']=='Poor']['steward'], 
                       y=df_merge_si[df_merge_si['health']=='Poor']['prop'])
                   )  ,row=2, col=1)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'palegreen',
                   name='Fair', 
                   showlegend = False,
                   x=df_merge_si[df_merge_si['health']=='Fair']['steward'], 
                   y=df_merge_si[df_merge_si['health']=='Fair']['prop'])
               )  ,row=2, col=1)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'lightsalmon' ,
                   name='Good', 
                   showlegend = False,
                   x=df_merge_si[df_merge_si['health']=='Good']['steward'], 
                   y=df_merge_si[df_merge_si['health']=='Good']['prop'])
           )  ,row=2, col=1)

# row2 col2 Bronx

   figure1.add_trace((
               go.Bar(
                       marker_color = 'lightskyblue' ,
                       name='Poor', 
                       showlegend = False,
                       x=df_merge_bx[df_merge_bx['health']=='Poor']['steward'], 
                       y=df_merge_bx[df_merge_bx['health']=='Poor']['prop'])
                   )  ,row=2, col=2)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'palegreen',
                   name='Fair', 
                   showlegend = False,
                   x=df_merge_bx[df_merge_bx['health']=='Fair']['steward'], 
                   y=df_merge_bx[df_merge_bx['health']=='Fair']['prop'])
               )  ,row=2, col=2)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'lightsalmon' ,
                   name='Good', 
                   showlegend = False,
                   x=df_merge_bx[df_merge_bx['health']=='Good']['steward'], 
                   y=df_merge_bx[df_merge_bx['health']=='Good']['prop'])
           )  ,row=2, col=2)
           
# row2 col2 Brookyln

   figure1.add_trace((
               go.Bar(
                       marker_color = 'lightskyblue' ,
                       name='Poor', 
                       showlegend = False,
                       x=df_merge_bk[df_merge_bk['health']=='Poor']['steward'], 
                       y=df_merge_bk[df_merge_bk['health']=='Poor']['prop'])
                   )  ,row=3, col=1)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'palegreen',
                   name='Fair', 
                   showlegend = False,
                   x=df_merge_bk[df_merge_bk['health']=='Fair']['steward'], 
                   y=df_merge_bk[df_merge_bk['health']=='Fair']['prop'])
               )  ,row=3, col=1)
   figure1.add_trace((
           go.Bar(
                   marker_color = 'lightsalmon' ,
                   name='Good', 
                   showlegend = False,
                   x=df_merge_bk[df_merge_bk['health']=='Good']['steward'], 
                   y=df_merge_bk[df_merge_bk['health']=='Good']['prop'])
           )  ,row=3, col=1)
   return figure1


   
      
if __name__ == '__main__':
    app.run_server(debug=True)
	