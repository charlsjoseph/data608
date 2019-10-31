import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#select distinct boronames
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=distinct(boroname)')
boroughs = pd.read_json(soql_url).sort_values(['boroname_1'], ascending=[True])

#select distinct species

soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=distinct(spc_common)')
spc_common = pd.read_json(soql_url).sort_values(['spc_common_1'], ascending=[True])

contigency_data = pd.read_csv("https://raw.githubusercontent.com/charlsjoseph/data608/master/module4/contigency_data.csv")


app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H2(children='New York City tree census - 2015',
                        className='nine columns')
            ], className="row"
        ),
            
    html.Div(
            [
                html.H3(children='Q1: Species Health Proportions',
                        className='nine columns')
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.H6('Choose Boroughs:'),
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
                html.Div([
                        dcc.Graph(
                            id='bar-graph'
                        )
                    ], className= 'twelve columns'),
                
            ], className="row"
        ), 
        html.Div(
            [   html.H3(children='Q2: Correlation between Steward v/s Health',
                        className='eight columns'),
                html.H6('Contigency bar plots',
                        className='eight columns'),
                html.Div([
                        dcc.Graph(
                            id='bar-chartb'
                        )
                    ], className= 'twelve columns'
                    ),
                html.H6('Choropleth Map',className= 'ten columns' ),
                html.Div([
                        html.Img(src=app.get_asset_url('ny_choropleth.png'))
                    ], className= 'five columns'),
                html.Div([
                        html.P('Chi Square P-Value = 0 ', style={'fontSize': 18} ),
                        html.P('Identified dependency between Steward and Health ', style={'fontSize': 18} ),
                        html.P('Choropleth shows Manhatten, Staten Island and Queens are highly correlated boroughs ', style={'fontSize': 18} )
                    ], className= 'five columns')
                
            ], className="row"),
           
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
    [Input('boroughs', 'value')])
def update_figureb(boroughs):
   
   figure = make_subplots(rows=2, cols=2, 
                start_cell="bottom-left")
# row1 col2 Manhatten

   figure.add_trace((
                   go.Bar(
                       marker_color='lightskyblue' , name='None', 
                       x=contigency_data[contigency_data['steward']=='None']['health'], 
                       y=contigency_data[contigency_data['steward']=='None']['prop'])
                   ),row=2, col=1)
   figure.add_trace((
                   go.Bar(
                       marker_color='palegreen' , name='1or2', 
                       x=contigency_data[contigency_data['steward']=='1or2']['health'], 
                       y=contigency_data[contigency_data['steward']=='1or2']['prop'])
                   ),row=2, col=2)
   figure.add_trace((
                   go.Bar(
                       marker_color='lightsalmon' , name='3or4', 
                       x=contigency_data[contigency_data['steward']=='3or4']['health'], 
                       y=contigency_data[contigency_data['steward']=='3or4']['prop'])
                   ),row=1, col=1)
   figure.add_trace((
                   go.Bar(
                       marker_color='red' , name='4orMore', 
                       x=contigency_data[contigency_data['steward']=='4orMore']['health'], 
                       y=contigency_data[contigency_data['steward']=='4orMore']['prop'])
                   ),row=1, col=2)
   figure.update_yaxes(range=[0, contigency_data['prop'].max()])

   return figure

   
      
if __name__ == '__main__':
    app.run_server(debug=True)
	