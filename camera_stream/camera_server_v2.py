from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from multiprocessing import Process, Queue, Event
import cv2
import base64
import time

#global vars
detect_queue = Queue()
boxes_queue = Queue()
detect_ready = Event()

def stream_process(detect_queue, boxes_queue):
    camera = CSICamera(width=640, height=640, capture_width=640, capture_height=640, capture_fps=30)
    frame = camera.read()
    app = Flask(__name__)
    app.config['LAZY_LOADING'] = False
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")
    start_stream_task = True
    
    def generate_frames():
        """capture camera frame and emit it to the stream"""
        global frame_encoded
        start_t = time.time()
        frames = 0
        while True:
            #reading time is around 8ms
            frame = camera.read()
            
            if  detect_ready.is_set() :
                if not boxes_queue.empty():
                    data = boxes_queue.get()
                    print(data['classes'])
                    print(data['boxes'])
                detect_queue.put(frame)
                detect_ready.clear()
                
            # # conversion to base64
            resized_frame = cv2.resize(frame, (320, 320), 
                                   interpolation = cv2.INTER_LINEAR)
            buffer =  bgr8_to_jpeg(resized_frame)
            frame_encoded = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('stream', frame_encoded)

    @app.route('/')
    def index():
        """render end return template"""
        return render_template('index.html')

    
    @socketio.on('connect')
    def connect(x):
        nonlocal start_stream_task
        print(f'Client connected: {request.sid}')
        if start_stream_task:
            """create and start stream in new thread"""
            socketio.start_background_task(target=generate_frames)
            print("startuje thread z streamem")
            start_stream_task = False
            
    socketio.run( app,host='0.0.0.0',port=5001, debug=False, allow_unsafe_werkzeug=True)
    
    
def sending_to_predict(detect_queue, boxes_queue):
    app = Flask(__name__)
    app.config['LAZY_LOADING'] = False
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    def generate_frames():
        """get frame from sream_process and emit it to the detect"""
        while True:
            if not detect_queue.empty():
                    frame = detect_queue.get()
                    buffer =  bgr8_to_jpeg(frame)
                    frame_encoded = base64.b64encode(buffer).decode('utf-8')
                    socketio.emit( 'detect', frame_encoded)
                    
    start_stream_task = True
    @socketio.on('connect')
    def connect(x):
        nonlocal start_stream_task
        print(f'Client connected: {request.sid}')
        if start_stream_task:
            """create and start stream in new thread"""
            socketio.start_background_task(target=generate_frames)
            print("startuje thread z streamem")
            start_stream_task = False

    @socketio.on('boxes')
    def boxes(data):
        boxes_queue.put(data)
        detect_ready.set()
    
    socketio.run( app,host='0.0.0.0',port=5005, debug=False, allow_unsafe_werkzeug=True)
    
if __name__ == '__main__':
    p1 = Process(target=stream_process, args=(detect_queue, boxes_queue))
    p2 = Process(target=sending_to_predict, args=(detect_queue, boxes_queue))

    p1.start()
    p2.start()

    p1.join()
    p2.join()