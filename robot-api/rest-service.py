#!/usr/bin/env python2.7
from ev3dev import ev3
from flask import Flask
from flask import request
from flask import Response
import time
import math
import threading

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
    - /drive?x=[x]&y=[y]
  Open and close the Claw
    - /grab
    - /release"""

    return Response(message, mimetype='text/plain')


@app.route("/forward")
def forward():
    print "Direction: forward"
    drive_motors_run_direct(50, 50)
    return "Going forward....\n"


@app.route("/backward")
def backward():
    print "Direction: backward"
    drive_motors_run_direct(-50, -50)
    return "Going backward....\n"


@app.route("/stop")
def stop():
    global rightMotor
    global leftMotor
    print "Stop"
    rightMotor = get_large_motor('outC')
    leftMotor = get_large_motor('outB')
    rightMotor.stop()
    leftMotor.stop()
    return "..stopping"


@app.route("/left")
def left():
    print "Direction: left"
    drive_motors_run_direct(-50, 50)
    return "Turning left....\n"


@app.route("/right")
def right():
    print "Direction: right"
    drive_motors_run_direct(50, -50)
    return "Turning right....\n"


@app.route("/forward_right")
def forward_right():
    print "Direction: forward and right"
    drive_motors_run_direct(100, 50)
    return "Driving forward and right....\n"


@app.route("/forward_left")
def forward_left():
    print "Direction: forward and left"
    drive_motors_run_direct(50, 100)
    return "Driving forward and left....\n"


@app.route("/backward_right")
def backward_right():
    print "Direction: backward and right"
    drive_motors_run_direct(-100, -50)
    return "Driving backward and right....\n"


@app.route("/backward_left")
def backward_left():
    print "Direction: backward and left"
    drive_motors_run_direct(-50, -100)
    return "Driving backward and left....\n"


@app.route("/drive")
def drive():
    x = request.args.get('x')
    y = request.args.get('y')

    radians = math.atan2(float(x), float(y))
    if 0 <= radians and radians < math.pi / 8 or radians > 15 * math.pi / 8:
        right()
    elif math.pi / 8 <= radians and radians < 3 * math.pi / 8:
        forward_right()
    elif 3 * math.pi / 8 <= radians and radians < 5 * math.pi / 8:
        forward()
    elif 5 * math.pi / 8 <= radians and radians < 7 * math.pi / 8:
        forward_left()
    elif 7 * math.pi / 8 <= radians and radians < 9 * math.pi / 8:
        left()
    elif 9 * math.pi / 8 <= radians and radians < 11 * math.pi / 8:
        backward_left()
    elif 11 * math.pi / 8 <= radians and radians < 13 * math.pi / 8:
        backward()
    elif 13 * math.pi / 8 <= radians and radians < 15 * math.pi / 8:
        backward_right()
    else:
        stop()

    wait_and_stop_drive_motors(2)
    return "Driving....\n"


@app.route("/grab")
def grab():
    global grabMotor
    grabMotor = get_large_motor('outA')
    grabMotor.position = 0
    motor_run_direct(grabMotor, 50)
    wait_and_stop_motor(grabMotor, 2)
    return "Grab....\n"


@app.route("/release")
def release():
    global grabMotor
    grabMotor = get_large_motor('outA')
    motor_run_direct(grabMotor, -50)
    wait_and_stop_motor(grabMotor, 2)
    return "Release...\n"


def drive_motors_run_direct(left_motor_speed, right_motor_speed):
    global rightMotor
    global leftMotor
    rightMotor = get_large_motor('outC')
    leftMotor = get_large_motor('outB')
    motor_run_direct(rightMotor, right_motor_speed)
    motor_run_direct(leftMotor, left_motor_speed)


def motor_run_direct(motor, motor_speed):
    """
    Executes run_direct command to motor at given speed
    :param motor:
    :param motor_speed:
    :return:
    """
    motor.duty_cycle_sp = motor_speed
    motor.run_direct()


def wait_and_stop_drive_motors(seconds_to_wait=2):
    """
    Waits given time in another thread and the stops the driving motors
    :param seconds_to_wait:
    :return:
    """
    global rightMotor
    global leftMotor
    rightMotor = get_large_motor('outC')
    leftMotor = get_large_motor('outB')
    wait_and_stop_motor(rightMotor, seconds_to_wait)
    wait_and_stop_motor(leftMotor, seconds_to_wait)


def wait_and_stop_motor(motor, seconds_to_wait=2):
    """
    Starts a thread which sleeps for a given time and the commands the motor given as parameter to stop
    :param motor:
    :param seconds_to_wait:
    :return:
    """
    thread = threading.Thread(target=wait_and_stop_motor_thread, args=(motor, seconds_to_wait,))
    thread.start()


def wait_and_stop_motor_thread(motor, seconds_to_wait):
    time.sleep(seconds_to_wait)
    motor.stop()


def get_large_motor(motor_address):
    return ev3.LargeMotor(motor_address)
    #return FakeMotor(motor_address)


class FakeMotor(object):
    """
    Class for testing the motor commands without ev3dev environment
    """
    def __init__(self, motor_name):
        self.duty_cycle_sp = 0
        self.motor_name = motor_name

    def run_direct(self):
        print "Motor " + self.motor_name + " runnig at speed of " + str(self.duty_cycle_sp)

    def stop(self):
        print "Motor " + self.motor_name + " stopped"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
