# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='New York City tree census - 2015',
                        className='nine columns')
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
                            options=[{'label': 'New York City', 'value': 'NYC'},
									 {'label': 'Montreal', 'value': 'MTL'},
									 {'label': 'San Francisco', 'value': 'SF'}],
							value='NYC',
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
                    ),
                html.Div(
                    [
                        html.P('Developed by Charls Joseph - ', style = {'display': 'inline'}),
                        html.A('charlsjoseph@gmail.com', href = 'mailto:charlsjoseph@gmail.com')
                    ], className = "twelve columns",
                       style = {'fontSize': 18, 'padding-top': 20}
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one'))


if __name__ == '__main__':
    app.run_server(debug=True)
	