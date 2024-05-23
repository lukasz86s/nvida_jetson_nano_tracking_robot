from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from engine_control import RobotMovement
import signal

left_pin_a = 20
left_pin_b = 21

right_pin_a = 26
right_pin_b = 19

robot_move = RobotMovement(left_pin_a, left_pin_b, right_pin_a, right_pin_b)
app = Flask(__name__)
#TODO: set secret key in os.env or in not tracking file
app.config['SECRET_KEY'] = 'secret!'

def forward(power):
    robot_move.forward(power)

def left(power):
    robot_move.left(power)

def right(power):
    robot_move.right(power)

def backward(power):
    robot_move.backward(power)

def stop():
    robot_move.stop()


def handle_sigint(sig, frame):
    print(sig)
    robot_move.kill_engines()
    exit(0)

@socketio.on('move')
def handel_move(data):
    direction = data.get('direction')
    power = data.get('power')

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


signal.signal(signal.SIGINT, handle_sigint)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False, allow_unsafe_werkzeug=True)