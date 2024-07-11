
from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg
from flask import Flask, render_template
from flask_socketio import SocketIO
import base64

#camera = cv2.VideoCapture(0)  # Numer urządzenia kamery (domyślnie 0)
camera = CSICamera(width=320, height=320, capture_width=640, capture_height=480, capture_fps=30)
frame = camera.read()
buffer =  bgr8_to_jpeg(frame)
detect_ready = False

frame_encoded = base64.b64encode(buffer).decode('utf-8')

app = Flask(__name__)
app.config['LAZY_LOADING'] = False
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

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

@socketio.on('boxes')
def boxes(data):
    print(data['classes'])
    print(data['boxes'])

#function for future exchanging data with yolo detector
@socketio.on('detect_ready')
def detect_ready():
    global detect_ready 
    detect_ready = True

if __name__ == '__main__':
    #debug off, when ON app is works incorrectly
    socketio.run( app,host='0.0.0.0',port=5001, debug=False, allow_unsafe_werkzeug=True)