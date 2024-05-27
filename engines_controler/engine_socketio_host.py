from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from engine_control import RobotMovement
import signal
import threading
import time

left_pin_a = 20
left_pin_b = 21

right_pin_a = 26
right_pin_b = 19

robot_move = RobotMovement(left_pin_a, left_pin_b, right_pin_a, right_pin_b)
app = Flask(__name__)
#TODO: set secret key in os.env or in not tracking file
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
message_time = time.time()
message_time_flag = 0


def handle_sigint(sig, frame):
    print(sig)
    robot_move.kill_engines()
    exit(0)

@socketio.on('move')
def handel_move(data):
    global message_time, message_time_flag
    direction = data.get('direction')
    power = data.get('power')
    message_time = time.time()
    message_time_flag = 1
        
    if direction == 'left':
        robot_move.left(power)
    if direction == 'right':
        robot_move.right(power)
    if direction == 'forward':
        robot_move.forward(power)
    if direction == 'backward':
        robot_move.backward(power)
    if direction == 'sotp':
        robot_move.stop()

def check_message_time():
    global message_time, message_time_flag
    while True:
        elapsed_time = time.time() - message_time
        if elapsed_time > 0.2 and message_time_flag:
            robot_move.stop()
            message_time_flag = 0
        time.sleep(0.05)

signal.signal(signal.SIGINT, handle_sigint)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    checker_thread = threading.Thread(target=check_message_time)
    checker_thread.daemon = True
    checker_thread.start()
    socketio.run(app, host='0.0.0.0', debug=False, allow_unsafe_werkzeug=True)
    