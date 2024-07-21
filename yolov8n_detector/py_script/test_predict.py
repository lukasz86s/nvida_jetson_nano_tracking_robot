from ultralytics import YOLO

model = YOLO('weights/last.pt')
photos = ['sign0.jpeg', 'sign7.jpeg', 'dog.jpeg']
i = 0
while True:
    result = model.predict(photos[i%3], conf=0.3, verbose=False)#, stream=True)
    #result = next(result)
    print(result[0].speed)
    i += 1