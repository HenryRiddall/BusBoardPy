from flask import Flask, render_template
from busAPI import getArrivals

app = Flask(__name__)


@app.route('/')
def hello():
    arrivals = getArrivals("490008660N")
    
    return render_template("index.html", arrivals=arrivals)