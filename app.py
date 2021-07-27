from flask import Flask
import pandas
from calculations import *
app = Flask(__name__)



@app.route("/")
def hello():
    df = pandas.read_csv("AUDJPY=X.csv")
    # histogram = histogram(df)
    atr = atr(df)
    print(df)
    return 

    
@app.route("/calculate", methods=['GET', 'POST'])
def calculate():
    return "<p>Hello</p>"