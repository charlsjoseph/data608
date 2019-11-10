

from flask import Flask, jsonify, render_template, request, url_for
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)
fetch_counties_query = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
    '$select=distinct(spc_common)' +\
    '&$where=spc_common is not null').replace(" ", '%20')
species = list(pd.read_json(fetch_counties_query).sort_values(['spc_common_1'], ascending=[True])['spc_common_1'])

fetch_borough_query = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
    '$select=distinct(boroname)')
boroughs = list(pd.read_json(fetch_borough_query).sort_values(['boroname_1'], ascending=[True])['boroname_1'])


	
@app.route("/test")
def test():
    return 'Success'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/get_species')
def get_species():
    return jsonify(species)

@app.route('/fetch_tree_data')
def fetch_tree_data():

    borough = request.args.get('borough') 
    species = request.args.get('species') 
    boroughLst = []
    boroughLst.append(borough)
    speciesLst = []
    speciesLst.append(species)
    print(boroughLst)
    print(speciesLst)

    fetch_tree_data_query = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
                    '$select=health , spc_common ,boroname ,count(tree_id)' +\
                    '&$where=boroname in ' + format(boroughLst) + ' and spc_common in ' + format(speciesLst) + ' ' +\
                    '&$group=health,spc_common,boroname').replace(' ', '%20')
    print(fetch_tree_data_query)
    soql_trees = pd.read_json(fetch_tree_data_query)
    soql_trees['boroname_and_species'] = soql_trees['boroname'] + ',' + soql_trees['spc_common']
    soql_trees = soql_trees.drop(columns=['spc_common', 'boroname'])
    soql_trees['health_ratio'] = soql_trees.groupby(['boroname_and_species'])['count_tree_id'].transform(lambda x: x/x.sum()*100)
    soql_trees = soql_trees.sort_values(['boroname_and_species'], ascending=[True])

    #data = {"health" : ["Good", "Poor" , "Fair"],"prop" : ["70", "10", "20"]}
    #boroughs = pd.DataFrame.from_dict(soql_trees)
    return soql_trees.to_json(orient='records')


@app.route('/get_boroughs')
def get_boroughs():
    return jsonify(boroughs)

def format(itemlist):
    #i/p List  ["Bronx", "Queens" ]
    #o/p String : ("Bronx", "Queens")
    tmpList = ['\"' + str(elm) + '\"' for elm in itemlist]
    return '(' + ', ' .join(tmpList) + ')'

if __name__ == "__main__":
    app.run()
