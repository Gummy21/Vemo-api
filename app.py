import json
import os
import pandas
from flask import Flask
from flask import request
from calculations import *
from flask_cors import CORS
from flask_compress import Compress
from werkzeug.middleware.proxy_fix import ProxyFix


compress = Compress()

app = Flask(__name__)
cors = CORS(app)
compress.init_app(app)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route("/")
def hello():
    data = pandas.read_csv("AUDJPY=X.csv")
    df = data.dropna().copy()
    stats ={
        "histogram":returns(df,"Daily"),
        "ATR":atr(df,"Daily")
    }
    stats = json.dumps(stats)
    
   
    return stats


    
@app.route("/calculate", methods=['POST'])
def calculate():
    # Check if csv
    df = pandas.read_csv(request.files["file"])
    timeframe = request.form['timeframe']
    stats = {
        "histogram":returns(df,timeframe),
        "ATR":atr(df,timeframe)
    }
    stats = json.dumps(stats)
    return stats

if __name__ == '__main__':
    print("Server started")
    app.run()