from flask import *
import json

app = Flask(__name__)


@app.route('/controller', methods=['GET'])
def controller():
    return render_template("templates/JoyStick/joy.html")


@app.route('/', methods=['GET'])
def default():
    return redirect(url_for('controller'))