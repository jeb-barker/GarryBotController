from flask import *
# import RPi.GPIO as GPIO

app = Flask(__name__)

leftMotorStatus = False
rightMotorStatus = False

PIN_RIGHT = 0
PIN_LEFT = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_LEFT, GPIO.OUT)
GPIO.setup(PIN_RIGHT, GPIO.OUT)


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
        GPIO.output(PIN_RIGHT, GPIO.HIGH)
    if leftMotorStatus:
        # left motor is on when it shouldn't be, update accordingly.
        print("left motor off")
        GPIO.output(PIN_LEFT, GPIO.LOW)

    return "Turn Left"


@app.route('/turnRight', methods=['POST'])
def turnRight():
    if rightMotorStatus:
        # right motor should be off.
        print("right motor off")
        GPIO.output(PIN_RIGHT, GPIO.LOW)
    if not leftMotorStatus:
        # left motor is off when it shouldn't be.
        print("left motor on")
        GPIO.output(PIN_LEFT, GPIO.HIGH)
    return "Turn Right"


@app.route('/zero', methods=['POST'])
def zero():
    if rightMotorStatus:
        # right motor should be off.
        print("right motor off")
        GPIO.output(PIN_RIGHT, GPIO.LOW)
    if leftMotorStatus:
        # left motor should be off.
        print("left motor off")
        GPIO.output(PIN_LEFT, GPIO.LOW)
    return "Stop Movement"


@app.route('/forward', methods=['POST'])
def forward():
    if not rightMotorStatus:
        # right motor is off when it shouldn't be.
        print("right motor on")
        GPIO.output(PIN_RIGHT, GPIO.HIGH)
    if not leftMotorStatus:
        # left motor is off when it shouldn't be.
        print("left motor on")
        GPIO.output(PIN_LEFT, GPIO.HIGH)
    return "Forward"
