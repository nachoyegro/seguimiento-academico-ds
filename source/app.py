# app.py - a minimal flask api using flask_restful
from flask import Flask, escape, request
from provider import DataProvider
from transformer import DataTransformer
import json
from config import app

@app.route('/')
def hello():
    data = DataProvider().retrieve_materiascursadas(username=app.config['USERNAME'], password=app.config['PASSWORD'])
    dataframe = DataTransformer(data).transform_to_dataframe()
    return dataframe

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')