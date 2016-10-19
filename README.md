# Techday 2016

More info at https://cinia.github.io/techday2016/presentation/

## Startup procedure

Run `python3 sensor-data-publisher/publish-data.py`

Run `node sensor-data-subscriber/subscriber.js`

Now there should be a webserver running on port 3000 with the sensor data displayed.

## Starting the OpenCV camera server

Run `python2 opencv-camera/cameraserver.py`

This starts a HTTP server on port 8000, and the camera's video feed processed through OpenCV can be accessed there.

## TODO:

 * Link control REST api to Web UI
 * ev3 sensor data to MQTT broker on RPi
 * OpenCV pipeline integration to Web UI
