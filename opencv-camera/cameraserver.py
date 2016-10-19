"""
A script that takes video feed from a Raspberry Pi camera, and hosts a webpage
that can be used to access the feed.

In addition, the feed is run through some OpenCV manipulation, although this
functionality is currently just at an example level.

Usage: 
1. call 'python2 opencv-camera/cameraserver.py'
2. Navigate to <rasp url>:8000 
3. Enjoy the stream
"""
import io
import picamera
import picamera.array
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import numpy
import cv2
from threading import Lock

HOST_PORT=8000
PAGE="""\
<html>
<head>
<title>I am robot</title>
</head>
<body style="background: #333">
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(picamera.array.PiRGBAnalysis):
    """
    Custom output class for Picamera. Gets video input from picamera, does OpenCV stuff to it, 
    then sends the image over HTTP to stream clients.
    """
    def __init__(self, camera):
        super(picamera.array.PiRGBAnalysis, self).__init__(camera)
        self.lock = Lock()
        self.frame = io.BytesIO()
        self.clients = []

    def analyse(self, img):
        """
        Called every frame with the image coverted into a numpy array. Sends
        the final image to streaming clients.
        """
        died = []
        
        buf = self.handle_image(img)
        
        #send to clients:
        with self.lock:
            for client in self.clients:
                try:
                    client.wfile.write(b'--FRAME\r\n')
                    client.send_header('Content-Type', 'image/jpeg')
                    client.send_header('Content-Length', str(len(buf)))
                    client.end_headers()
                    client.wfile.write(bytearray(buf))
                    client.wfile.write(b'\r\n')
                except Exception as e:
                    print e
                    died.append(client)
        if died:
            self.remove_clients(died)
            
    def handle_image(self, image):
        """
        !! Do OpenCV magic here !! 
        
        Code below is an example that just grayscales the image.
        
        This is called every frame, image is the frame as a numpy array that OpenCV should
        understand.
        
        This needs to return the final image encoded as jpeg.
        """
        data = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, buf = cv2.imencode('.jpg', data)
        return buf
        

    def flush(self):
        """
        Flush client streams.
        """
        with self.lock:
            for client in self.clients:
                client.wfile.close()

    def add_client(self, client):
        """
        Add a new streaming client.
        """
        print('Adding streaming client %s:%d' % client.client_address)
        with self.lock:
            self.clients.append(client)

    def remove_clients(self, clients):
        """
        Remove one or more streaming clients.
        """
        with self.lock:
            for client in clients:
                try:
                    print('Removing streaming client %s:%d' % client.client_address)
                    self.clients.remove(client)
                except ValueError:
                    pass # already removed

class StreamingHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Handles requests to the server, send the web page and add
    the requester as a stream client.
    """
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.close_connection = False
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=--FRAME')
            self.end_headers()
            output.add_client(self)
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """
    Just a default implementation of the BaseHTTPServer, that gets passed the
    StreamingHandler as a request handler.
    """
    pass

with picamera.PiCamera(resolution='640x480', framerate=16) as camera:
    output = StreamingOutput(camera)
    camera.start_recording(output, format='bgr')
    try:
        address = ('', HOST_PORT)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
