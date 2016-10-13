#!/usr/bin/env python

import sys
import time
import paho.mqtt.client as mqtt
import argparse
from sense_hat import SenseHat

parser = argparse.ArgumentParser(description="Publish all the sensor data!")
parser.add_argument("--host", default="localhost", help="broker address (default is localhost)")
parser.add_argument("--port", default="1883", help="broker port (default is 1883)")
parser.add_argument("--interval", default="1", help="sensor data publishing interval in seconds (default 1)")

args = parser.parse_args()
broker_url = args.host
broker_port = int(args.port)

sense = SenseHat()
client = mqtt.Client()
client.connect(broker_url, broker_port, 60)

while True:
  temp = sense.get_temperature()
  humidity = sense.get_humidity()
  pressure = sense.get_pressure()
  temp_from_hum = sense.get_temperature_from_humidity()
  temp_from_press = sense.get_temperature_from_pressure()
  orientation = sense.get_orientation_degrees()
  compass = sense.get_compass()
  gyro = sense.get_gyroscope()
  accelerometer = sense.get_accelerometer()

  client.publish("robot/senses/temperature", temp)
  client.publish("robot/senses/humidity/humidity", humidity)
  client.publish("robot/senses/humidity/temperature", temp_from_hum)
  client.publish("robot/senses/pressure/pressure", pressure)
  client.publish("robot/senses/pressure/temperature", temp_from_press)
  client.publish("robot/senses/orientation/pitch", orientation["pitch"])
  client.publish("robot/senses/orientation/roll", orientation["roll"])
  client.publish("robot/senses/orientation/yaw", orientation["yaw"])
  client.publish("robot/senses/compass", compass)
  client.publish("robot/senses/gyroscope/pitch", gyro["pitch"])
  client.publish("robot/senses/gyroscope/roll", gyro["roll"])
  client.publish("robot/senses/gyroscope/yaw", gyro["yaw"])
  client.publish("robot/senses/accelerometer/pitch", accelerometer["pitch"])
  client.publish("robot/senses/accelerometer/roll", accelerometer["roll"])
  client.publish("robot/senses/accelerometer/yaw", accelerometer["yaw"])
  time.sleep(float(args.interval))

client.disconnect()
