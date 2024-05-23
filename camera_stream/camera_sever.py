
from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg
from flask import Flask, render_template
from flask_socketio import SocketIO
import base64

#camera = cv2.VideoCapture(0)  # Numer urządzenia kamery (domyślnie 0)
camera = CSICamera(width=224, height=224, capture_width=1280, capture_height=720, capture_fps=30)
frame = camera.read()
buffer =  bgr8_to_jpeg(frame)

frame_encoded = base64.b64encode(buffer).decode('utf-8')

#import cv2
app = Flask(__name__)
app.config['LAZY_LOADING'] = False
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def generate_frames():
    global frame_encoded
    """capture camera frame and emit it to the stream"""
    while True:
        frame = camera.read()
        # # conversion to base64
        buffer =  bgr8_to_jpeg(frame)
        frame_encoded = base64.b64encode(buffer).decode('utf-8')
        # sendig encoded frmae 
        socketio.emit('stream', frame_encoded)


# Endpoint video stream
@app.route('/')
def index():
    """render end return template"""
    return render_template('index.html')

@socketio.on('connect')
def connect():
    """create and start stream in new thread"""
    socketio.start_background_task(target=generate_frames)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False, allow_unsafe_werkzeug=True)