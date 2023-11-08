from flask import *
import mysql.connector
import json

app = Flask(__name__)

credentials = json.load(open("credentials.json", "r"))


@app.route('/controller', methods=['GET'])
def controller():
    return render_template("controller.html")


@app.route('/', methods=['GET'])
def default():
    return redirect(url_for('controller'))