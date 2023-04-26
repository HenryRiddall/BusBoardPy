from flask import Flask, render_template, request
from busAPI import get_stop_points

app = Flask(__name__)


@app.route('/', methods=('GET','POST'))
def hello():
    postcode = request.form.get("postcode")
    stop_points = get_stop_points(postcode)
    
    
    return render_template("index.html", stop_points=stop_points, postcode=postcode)

