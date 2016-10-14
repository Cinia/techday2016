#!/usr/bin/env python2.7
#from ev3dev import ev3
from flask import Flask
from flask import request
import time
import math

app = Flask(__name__)

@app.route("/")
def hello():
    message = """Hello, this is the command-api for robot. Available commands (endpoints) are:
  With these robot just runs to given direction until stop command is given
    - /forward
    - /backward
    - /left
    - /right
    - /forward_left
    - /forward_right
    - /backward_left
    - /backward_right
    - /stop
  Decides the direction to run based on direction from origo to x,y location, runs 2 seconds towards that direction
    - /drive?x=[x]&y=[y]"""

    return message

@app.route("/forward")
def forward():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=50
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=50
    leftMotor.run_direct()
    return "Going forward...."

@app.route("/backward")
def backward():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=-50
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=-50
    leftMotor.run_direct()
    return "Going forward...."

@app.route("/stop")
def stop():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.stop()
    leftMotor.stop()
    return "..stopping"

@app.route("/left")
def left():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=50
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=-50
    leftMotor.run_direct()
    return "Turning left...."

@app.route("/right")
def right():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=-50
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=50
    leftMotor.run_direct()
    return "Turning right...."

@app.route("/forward_right")
def forward_right():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=50
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=100
    leftMotor.run_direct()
    return "Driving forward and right...."

@app.route("/forward_left")
def forward_left():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=100
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=50
    leftMotor.run_direct()
    return "Driving forward and left...."

@app.route("/backward_right")
def backward_right():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=-50
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=-100
    leftMotor.run_direct()
    return "Driving backward and right...."

@app.route("/backward_left")
def backward_left():
    global rightMotor
    global leftMotor
#    rightMotor=ev3.LargeMotor('outC')
#    leftMotor=ev3.LargeMotor('outB')
    rightMotor.duty_cycle_sp=-100
    rightMotor.run_direct()
    leftMotor.duty_cycle_sp=-50
    leftMotor.run_direct()
    return "Driving backward and left...."

@app.route("/drive")
def drive():
    global x
    global y
    global radians

    x=request.args.get('x')
    y=request.args.get('y')

    radians = math.atan2(float(x),float(y))
    if (0 <= radians and radians < math.pi / 8 or radians > 15 * math.pi / 8):
        right()
    elif (math.pi / 8 <= radians and radians < 3 * math.pi / 8):
        forward_right()
    elif (3 * math.pi / 8 <= radians and radians < 5 * math.pi / 8):
        forward()
    elif (5 * math.pi / 8 <= radians and radians < 7 * math.pi / 8):
        forward_left()
    elif (7 * math.pi / 8 <= radians and radians < 9 * math.pi / 8):
        left()
    elif (9 * math.pi / 8 <= radians and radians < 11 * math.pi / 8):
        backward_left()
    elif (11 * math.pi / 8 <= radians and radians < 13 * math.pi / 8):
        backward()
    elif (13 * math.pi / 8 <= radians and radians < 15 * math.pi / 8):
        backward_right()
    else:
        stop()
    
    time.sleep(2)
    stop()
    return "Driving...."

@app.route("/grab")
def grab():
    global grabMotor
#    grabMotor=ev3.Motor('outA')
    grabMotor.position=0
    grabMotor.duty_cycle_sp=50
    grabMotor.run_direct()
    time.sleep(2)
    grabMotor.stop()
    return "Grab...."

@app.route("/release")
def release():
    global grabMotor
#    grabMotor=ev3.Motor('outA')
    grabMotor.duty_cycle_sp=-50
    grabMotor.run_direct()
    time.sleep(2)
    grabMotor.stop()
    return "Release...."

if __name__ == "__main__":
    app.run(host='0.0.0.0')
