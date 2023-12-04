import time

from flask import *
import pigpio
import RPi.GPIO as GPIO
# import RPi.GPIO as GPIO

app = Flask(__name__)

leftMotorStatus = False
rightMotorStatus = False
armed = False

PIN_RIGHT = 0
PIN_LEFT = 0
PIN_BLADES = 27
pi = pigpio.pi()

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
    global rightMotorStatus
    global leftMotorStatus
    if not rightMotorStatus:
        # right motor should be on.
        print("right motor on")
        GPIO.output(PIN_RIGHT, GPIO.HIGH)
        rightMotorStatus = True
    if leftMotorStatus:
        # left motor is on when it shouldn't be, update accordingly.
        print("left motor off")
        GPIO.output(PIN_LEFT, GPIO.LOW)
        leftMotorStatus = False

    return "Turn Left"


@app.route('/turnRight', methods=['POST'])
def turnRight():
    global rightMotorStatus
    global leftMotorStatus
    if rightMotorStatus:
        # right motor should be off.
        print("right motor off")
        GPIO.output(PIN_RIGHT, GPIO.LOW)
        rightMotorStatus = False
    if not leftMotorStatus:
        # left motor is off when it shouldn't be.
        print("left motor on")
        GPIO.output(PIN_LEFT, GPIO.HIGH)
        leftMotorStatus = True
    return "Turn Right"


@app.route('/zero', methods=['POST'])
def zero():
    global rightMotorStatus
    global leftMotorStatus
    if rightMotorStatus:
        # right motor should be off.
        print("right motor off")
        GPIO.output(PIN_RIGHT, GPIO.LOW)
        rightMotorStatus = False
    if leftMotorStatus:
        # left motor should be off.
        print("left motor off")
        GPIO.output(PIN_LEFT, GPIO.LOW)
        leftMotorStatus = False
    return "Stop Movement"


@app.route('/forward', methods=['POST'])
def forward():
    global rightMotorStatus
    global leftMotorStatus
    if not rightMotorStatus:
        # right motor is off when it shouldn't be.
        print("right motor on")
        GPIO.output(PIN_RIGHT, GPIO.HIGH)
        rightMotorStatus = True
    if not leftMotorStatus:
        # left motor is off when it shouldn't be.
        print("left motor on")
        GPIO.output(PIN_LEFT, GPIO.HIGH)
        leftMotorStatus = True
    return "Forward"


@app.route('/arm_blades', methods=['POST'])
def arm():
    global armed
    if not armed:
        pi.set_servo_pulsewidth(PIN_BLADES, 1000)  # Minimum throttle.
        time.sleep(1)
        pi.set_servo_pulsewidth(PIN_BLADES, 2000)  # Maximum throttle.
        time.sleep(1)
        pi.set_servo_pulsewidth(PIN_BLADES, 1100)  # Slightly open throttle.
        time.sleep(1)
        pi.set_servo_pulsewidth(PIN_BLADES, 0)  # Stop servo pulses.
        #that sequence of pulses should arm the ESC/motor for future use.


@app.route('/change_throttle', methods=['POST'])
def throttle():
    global armed
    data = request.form
    print(data)
    if armed:
        throttleLevel = data.level
        pi.set_servo_pulsewidth(PIN_BLADES, throttleLevel)


