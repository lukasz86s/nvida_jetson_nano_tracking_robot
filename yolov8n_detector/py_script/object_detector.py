import os
import cv2
from ultralytics import YOLO
HOME = os.getcwd()
model = YOLO(f'{HOME}/weights/last.pt')
import numpy as np
import base64
import socketio 
import time

#import torch
#print(torch.cuda.is_available())

b = model.predict(f'{HOME}/dog.jpeg', conf=0.5, verbose=False)
classes = list(b[0].names.values())
sio = socketio.Client()

def predict(img):
    data = model.predict(img, conf=0.3, verbose=False)
    obj_cls =  [classes[i] for i in data[0].boxes.cls.int()]
    boxes = data[0].boxes.xyxy.cpu().int().numpy().tolist()
    print(data[0].speed)
    return obj_cls, boxes

@sio.on('detect')
def handle_stream(data):
    print('odbieram')
    decode_data = base64.b64decode(data)
    img = cv2.imdecode(np.frombuffer(decode_data,dtype=np.uint8), cv2.IMREAD_COLOR)
    cls_, boxes = predict(img)
    sio.emit('boxes',{'classes':cls_, 'boxes':boxes})

@sio.event
def connect():
    print('Connection established')
    sio.emit('boxes',{'classes':["test",], 'boxes':[0,0,0,0]})

if __name__ == '__main__':
    sio.connect('http://192.168.100.129:5005')
    #start broadcast
    sio.wait()