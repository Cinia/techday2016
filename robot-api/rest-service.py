#!/usr/bin/env python2.7
from ev3dev import ev3
from Queue import Queue, Empty

from flask import Flask
from flask import request
from flask import Response
import time
import math
import threading

app = Flask(__name__)


class FakeMotor(object):
    """
    Class for testing the motor commands without ev3dev environment
    """
    def __init__(self, motor_name):
        self.duty_cycle_sp = 0
        self.motor_name = motor_name

    def run_direct(self):
        print "Motor " + self.motor_name + " running at speed of " + str(self.duty_cycle_sp)

    def stop(self):
        print "Motor " + self.motor_name + " stopped"


def get_large_motor(motor_address):
    return ev3.LargeMotor(motor_address)
    #return FakeMotor(motor_address)


right_motor = get_large_motor('outC')
left_motor = get_large_motor('outB')
grab_motor = ev3.Motor('outA')

robot_command_queue = Queue()


def command_drive_motors_thread():
    """
    Listens for robot_command_queue for motor speed commands and commands motors to move accordingly.

    Motors are stopped after 2-3 seconds (5 ticks) if no further commands are given.

    Command read from Queue is tuple containing left motor speed and right motor speed, for example
        command = (50, 100)
        command = (None, 75)
        etc..
    :return:
    """

    ticks_left = 0
    motors_running = False

    print "Thread: the thread is starting"
    while True:
        time.sleep(0.5)
        try:
            if motors_running:
                # print "Thread: Peek if there is command in queue"
                command = robot_command_queue.get_nowait()
            else:
                # print "Thread: Wait for command from queue"
                command = robot_command_queue.get()
            # print "Thread: Got command:\n\t- left motor: " + str(command[0]) + "\n\t- right motor: " + str(command[1])
            if command[0] is not None:
                motor_run_direct(left_motor, command[0])

            if command[1] is not None:
                motor_run_direct(left_motor, command[1])

            ticks_left = 4
            motors_running = True
            robot_command_queue.task_done()
        except Empty:
            # print "Thread: Nothing to do.."
            if ticks_left <= 0:
                # print "Thread: Out of ticks, stop the thing"
                motor_stop(left_motor)
                motor_stop(right_motor)
                motors_running = False
            else:
                ticks_left -= 1
                # print "Thread: ticks: " + str(ticks_left)
            pass


thread = threading.Thread(target=command_drive_motors_thread)
print "Starting the thread"
thread.start()


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
  Decides the direction to run based on direction from 0,0 to x,y location, runs 2 seconds towards that direction
    - /drive?x=[x]&y=[y]
  To command drive motors individually use
    - /motors/left_motor?speed=50
    - /motors/right_motor?speed=75
  Open and close the Claw
    - /grab
    - /release
"""

    return Response(message, mimetype='text/plain')


def drive_motors_run_direct(left_motor_speed, right_motor_speed):
    robot_command_queue.put_nowait((left_motor_speed, right_motor_speed))


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
    motor_stop(left_motor)
    motor_stop(right_motor)
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

    return "Driving....\n"


@app.route("/grab")
def grab():
    motor_run_direct(grab_motor, 100)
    time.sleep(1)
    motor_stop(grab_motor)
    return return_no_content()


@app.route("/release")
def release():
    motor_run_direct(grab_motor, -100)
    time.sleep(1)
    motor_stop(grab_motor)
    return return_no_content()


def motor_stop(motor):
    motor.stop()


def return_no_content():
    return Response(None, 204)


@app.route("/motors/right_motor")
def set_right_motor_speed():
    motor_speed = request.args.get('speed')
    drive_motors_run_direct(None, motor_speed)
    return return_no_content()


@app.route("/motors/left_motor")
def set_left_motor_speed():
    motor_speed = request.args.get('speed')
    drive_motors_run_direct(motor_speed, None)
    return Response(None, 204)


def motor_run_direct(motor, motor_speed):
    """
    Executes run_direct command to motor at given speed
    :param motor:
    :param motor_speed:
    :return:
    """
    motor.duty_cycle_sp = motor_speed
    motor.run_direct()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
