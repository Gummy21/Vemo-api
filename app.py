from flask import Flask
import pandas
app = Flask(__name__)



@app.route("/")
def hello():
    df = pandas.read_csv("AUDUSD=X.csv")
    print(df)
    return 

    
@app.route("/calculate", methods=['GET', 'POST'])
def calculate():
    return "<p>Hello</p>"