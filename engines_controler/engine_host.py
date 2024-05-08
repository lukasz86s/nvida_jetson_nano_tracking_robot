from flask import Flask, request, jsonify
from engine_control import RobotMovement
import signal

left_pin_a = 20
left_pin_b = 21

right_pin_a = 26
right_pin_b = 19

robot_move = RobotMovement(left_pin_a, left_pin_b, right_pin_a, right_pin_b)
app = Flask(__name__)

def run_test(power):
    print("testowy starta, moc:", power)

@app.route('/forward', methods=['POST'])
def forward():
    data = request.json
    power = data.get("power")
    
    if power is None or (0 > power > 10):
        return jsonify({"error": "Invalid power value. must be between 0 to 10"}), 400
    
    robot_move.forward(power)
    return jsonify({"Ok": "engine run "}), 200

@app.route('/left', methods=['POST'])
def left():
    data = request.json
    power = data.get("power")
    
    if power is None or (0 > power > 10):
        return jsonify({"error": "Invalid power value. must be between 0 to 10"}), 400
    
    robot_move.left(power)
    return jsonify({"Ok": "engine run "}), 200

@app.route('/right', methods=['POST'])
def right():
    data = request.json
    power = data.get("power")
    
    if power is None or (0 > power > 10):
        return jsonify({"error": "Invalid power value. must be between 0 to 10"}), 400
    
    robot_move.right(power)
    return jsonify({"Ok": "engine run "}), 200

@app.route('/back', methods=['POST'])
def back():
    data = request.json
    power = data.get("power")
    
    if power is None or (0 > power > 10):
        return jsonify({"error": "Invalid power value. must be between 0 to 10"}), 400
    
    robot_move.backward(power)
    return jsonify({"Ok": "engine run "}), 200

@app.route('/stop', methods=['POST'])
def stop():
    robot_move.stop()
    return jsonify({"Ok": "engine stop "}), 200

def handle_sigint(sig, frame):
    robot_move.kill_engines()
    exit(0)
    
signal.signal(signal.SIGINT, handle_sigint)

if __name__ == '__main__':
    app.run(host='192.168.100.129', port=5000, debug=True)