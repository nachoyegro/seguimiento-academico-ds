# app.py - a minimal flask api using flask_restful
from flask import Flask, escape, request
from provider import DataProvider
import json

app = Flask(__name__)

@app.route('/')
def hello():
    data = DataProvider().retrieve_alumnos(username='', password='')
    return json.dumps(data)   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')