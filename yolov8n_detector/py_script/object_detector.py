import os
import cv2
from ultralytics import YOLO
HOME = os.getcwd()
model = YOLO(f'{HOME}/yolov8n.pt')
import numpy as np
import base64
import socketio 
import time
import torch

print(torch.cuda.is_available())

b = model.predict(f'{HOME}/dog.jpeg', conf=0.5, verbose=False)
classes = list(b[0].names.values())
sio = socketio.Client()

def predict(img):
    data = model.predict(img, conf=0.1, verbose=False)
    obj_cls =  [classes[i] for i in data[0].boxes.cls.int()]
    boxes = data[0].boxes.xyxy.cpu().int().numpy().tolist()
    print(data[0].speed)
    return obj_cls, boxes

cls_, boxes = predict(f'{HOME}/dog.jpeg')
start_time = time.time()
@sio.on('stream')
def handle_stream(data):
    global start_time
    time_ = time.time()
    if time_ - start_time > 1.5:
        decode_data = base64.b64decode(data)
        img = cv2.imdecode(np.frombuffer(decode_data,dtype=np.uint8), cv2.IMREAD_COLOR)
        cls_, boxes = predict(img)
        sio.emit('boxes',{'classes':cls_, 'boxes':boxes})
        start_time = time_

if __name__ == '__main__':
    sio.connect('http://192.168.100.129:5001')
    sio.wait()