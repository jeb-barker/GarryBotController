from flask import *
# import RPi.GPIO as GPIO

app = Flask(__name__)

leftMotorStatus = False
rightMotorStatus = False

@app.route('/controller', methods=['GET'])
def controller():
    return render_template("joy.html")


@app.route('/', methods=['GET'])
def default():
    return redirect(url_for('controller'))


@app.route('/joy.js')
def favicon():
    return redirect(url_for('static', filename='joy.js'))


@app.route('/turnLeft', methods=['POST'])
def turnLeft():
    if not rightMotorStatus:
        # right motor should be on.
        print("right motor on")
    if leftMotorStatus:
        # left motor is on when it shouldn't be, update accordingly.
        print("left motor off")

    return "Turn Left"


@app.route('/turnRight', methods=['POST'])
def turnRight():
    if rightMotorStatus:
        # right motor should be off.
        print("right motor off")
    if not leftMotorStatus:
        # left motor is off when it shouldn't be.
        print("left motor on")
    return "Turn Right"


@app.route('/zero', methods=['POST'])
def zero():
    if rightMotorStatus:
        # right motor should be off.
        print("right motor off")
    if leftMotorStatus:
        # left motor should be off.
        print("left motor off")
    return "Stop Movement"


@app.route('/forward', methods=['POST'])
def forward():
    if not rightMotorStatus:
        # right motor is off when it shouldn't be.
        print("right motor on")
    if not leftMotorStatus:
        # left motor is off when it shouldn't be.
        print("left motor on")
    return "Forward"
