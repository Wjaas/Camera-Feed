from flask import Flask, Response
import threading
from picamera2.picamera2 import Picamera2
import numpy as np
import cv2
import time

app = Flask(__name__)

frame = None
lock = threading.Lock()

# Load the Haar cascade file
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

def capture_frames():
    global frame, lock
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    picam2.start()

    while True:
        with lock:
            raw_frame = picam2.capture_array()
            frame = process_frame(raw_frame)
        time.sleep(1 / 30)  # Limiting to 30 FPS

def process_frame(raw_frame):
    """Detect faces and draw rectangles around them."""
    # Convert the frame to grayscale
    gray = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(raw_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return raw_frame

thread = threading.Thread(target=capture_frames, args=())
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Live Camera Stream with Face Detection</title>
    </head>
    <body>
        <center><h1>Live Camera Stream with Face Detection</h1></center>
        <center><img src="/stream"></center>
    </body>
    </html>
    """

def generate_frames():
    global frame, lock
    while True:
        with lock:
            if frame is None:
                continue
            success, encoded_image = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if not success:
                continue
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')

@app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
