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

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    file = request.files["file"]
    print(file)
    if file.filename == '':
        return ('No selected file')
    elif file and allowed_file(file.filename):

        df = pandas.read_csv(file)
        timeframe = request.form['timeframe']
        stats = {}
        if returns(df,timeframe)[0] & atr(df,timeframe)[0]:
            print("heloo")
            stats = {
                "histogram":returns(df,timeframe)[1],
                "ATR":atr(df,timeframe)[1]
            }
        else :
           print("dwqdq")
           stats = {
                "Error":"Double check the data is in the right format"
            }   
        
        
        
        stats = json.dumps(stats)
        return stats
    else :
        error = ["Only csv files are accepted"]
        return error
  

if __name__ == '__main__':
    print("Server started")
    app.run()