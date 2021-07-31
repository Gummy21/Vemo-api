from flask import Flask
from flask import request
import pandas
from calculations import *
from flask_compress import Compress

compress = Compress()

app = Flask(__name__)
compress.init_app(app)

@app.route("/")
def hello():
    df = pandas.read_csv("AUDJPY=X.csv")
    stats = {
        "histogram":histogram(df),
        "ATR":atr(df,"Daily")
    }

    return stats


    
@app.route("/calculate", methods=['POST'])
def calculate():
    df = pandas.read_csv(request.files['file'])
    timeframe = request.form['timeframe']
    stats = {
        "histogram":histogram(df),
        "ATR":atr(df,timeframe)
    }

    return stats