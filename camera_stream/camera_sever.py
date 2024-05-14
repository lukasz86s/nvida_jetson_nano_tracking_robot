from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
camera = cv2.VideoCapture(0)  # Numer urządzenia kamery (domyślnie 0)

def generate_frames():
    """capture camera frame and emit it to the stream"""
    while True:
        success, frame = camera.read()
        #TODO: think about handling frame read failure
        if not success:
            break
        else:
            # conversion to base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_encoded = base64.b64encode(buffer).decode('utf-8')
            # sendig encoded frmae 
            socketio.emit('stream', frame_encoded)
    camera.release()

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
    socketio.run(app, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)