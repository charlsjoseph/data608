

from flask import Flask, jsonify, render_template, request, url_for
import csv
import pandas as pd
import numpy as np
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
yearlyData = pd.read_csv('data/yearlyPolutiondata.csv')
toppolutedCounties = pd.read_csv('data/topcounties.csv')
monthly_all_states = pd.read_csv('data/monthly_all_states.csv')

@app.route("/test")
def test():
    return 'Success'


@app.route('/fetch_pol_data')

def fetch_pol_data():

    year = request.args.get('year') 

    filteredDF = yearlyData[yearlyData['year'] == int(year)]
    response  = {}
    for index, row in filteredDF.iterrows():
        innermap ={}
        innermap['AQI'] = row['AQI']
        innermap['NO2 AQI'] = row['NO2 AQI']
        innermap['O3 AQI'] = row['O3 AQI']
        innermap['SO2 AQI'] = row['SO2 AQI']
        innermap['CO AQI'] = row['CO AQI']
        response[row['State']] = innermap
    return json.dumps(response, indent=2, sort_keys=True)

@app.route('/toppolutedcounties')

def toppolutedcounties():

    filteredDF = toppolutedCounties.head(20)
    return filteredDF.to_json(orient='records')

@app.route('/')
def index():
    return render_template('index.html')

def appendZero(month):
    formated = '0' + str(month)  if len(str(month)) ==1 else str(month)
    return formated

@app.route('/monthlydata')

def monthlydata():
    state = request.args.get('state') 
    county = request.args.get('county') 

    filteredDF = monthly_all_states[(monthly_all_states['State'] == state) & (monthly_all_states['County'] == county) ]
    filteredDF['month'] =  filteredDF['month'].apply(appendZero)
    filteredDF['month'] = filteredDF['year'].astype('str') + '-' +  filteredDF['month']
    filteredDF = filteredDF.drop(columns = ['year'])
    return filteredDF.to_json(orient='records')


if __name__ == "__main__":
    app.run()
