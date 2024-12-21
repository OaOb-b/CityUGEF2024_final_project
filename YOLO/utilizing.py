from ultralytics import YOLO
import numpy as np
import cv2
from time import time, sleep
from datetime import datetime, timedelta
from threading import Thread, Lock
from collections import deque
from ultralytics.solutions import object_counter
import shelve
import os
from pathlib import Path

mapping = ['Onion',
'beef',
'chicken',
'eggs',
'potato',
'radish',
'garlic',
'lettuce',
'tomato']


FRIDGE = shelve.open('Fridge/FRIDGE', writeback= True)
# FRIDGE['Onion'] = deque()
# FRIDGE['beef'] = deque()
# FRIDGE['chicken'] = deque()
# FRIDGE['eggs'] = deque()
# FRIDGE['potato'] = deque()
# FRIDGE['radish'] = deque()
# FRIDGE['garlic'] = deque()
# FRIDGE['lettuce'] = deque()
# FRIDGE['tomato'] = deque()
# print(dict(FRIDGE))
# FRIDGE.close()



class ObjectDetection:

    def __init__(self, capture_index):
       
        self.capture_index = capture_index
                
        self.model = self.load_model()
        print('hi')
    
    def load_model(self):
       
        model = YOLO('./model/best_1.pt')  # load a pretrained YOLOv8n model
        model.fuse()
    
        return model

    def predict(self, frame):
       
        results = self.model(frame)
        
        return results
    

    def plot_bboxes(self, results, frame):
        class_ids = []
        
         # Extract detections for person class
        for result in results:
            boxes = result.boxes.cpu().numpy()
            class_ids.append(boxes.cls.astype(int))


        return results[0].plot(), class_ids

    def stock(self, ids):
        ids = ids[0]
        for Id in list(ids):
            ingredient = INGREDIENT(Id, 1/4320, datetime.now())  # 20 seconds span
            hashh = mapping[Id]
            FRIDGE[hashh].append(ingredient)


    def consume(self, ids):
        ids = ids[0]
        for Id in list(ids):
            hashh = mapping[Id]
            if FRIDGE[hashh]:
                FRIDGE[hashh].popleft()
                

    def __call__(self, mode):
        last_s = 0
        cap = cv2.VideoCapture(self.capture_index)
        
        # Loop through the video frames
        while cap.isOpened():
            

            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLO inference on the frame
                results = self.predict(frame)

                # Visualize the results on the frame
                annotated_frame, ids = self.plot_bboxes(results, frame)
                
                p = Path('dummy_path')  # Create a dummy path object
                im = frame  # The preprocessed image is the same as the original frame in this case
                im0 = frame.copy()  # Create a copy of the frame for visualization
                s = self.model.predictor.write_results(0, p, im, results)
                s = s[s.find(' ', 3) + 1]

                if s != last_s:
    
                    if mode:
                        self.stock(ids)
                    else:
                        self.consume(ids)
                
                last_s = s

                 # Display the annotated frame
                cv2.imshow("YOLO Inference", annotated_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                
            else:
                break
                
        cap.release()
        cv2.destroyAllWindows()
    

            
    
class INGREDIENT:
    def __init__(self, Id, span, inbound_datetime):
        self.id = Id
        self.span = span
        self.inbound_datetime = inbound_datetime
        self.expiration_datetime = inbound_datetime + timedelta(days= span)

    def get_id(self):
        return self.id

    def get_expiration(self):
        return self.expiration_datetime
                
def get_stock(fridge):
    hashmap = {}
    for ingredients in dict(fridge).values():
        for i in ingredients:
            iid  = mapping[i.get_id()] 
            
            if iid not in hashmap:
                hashmap[f'{iid}'] = 1
            else:
                hashmap[f'{iid}'] += 1
        
    print(hashmap)
    
    

def main(fridge):
    while True:
        for ingredients in dict(fridge).values():
            for ingredient in ingredients:
                d = ingredient.get_expiration()
                current = datetime.now()
                if current >= d:
                    print("*****************")
                    print('expired')
                    print("*****************")
        sleep(7)


t = Thread(target= main, args= (FRIDGE, ))
t.daemon = True
t.start()

def AskForInput():
    choice = input('1: put things into the fridge\n2: get things out of the fridge\n3: show stocks of the fridge\n4: turn off the fridge\n5: empty the fridge (test mode cheat code)\n->')

    if choice == '1':
        ObjectDetection(1)(1)

    elif choice == '2':
        ObjectDetection(1)(0)

    elif choice == '3':
        os.system('cls||clear')
        get_stock(FRIDGE) 
        input('Press any to continue')

    elif choice == '4':
        FRIDGE.close()
        return
        
    else:
        FRIDGE['Onion'] = deque()
        FRIDGE['beef'] = deque()
        FRIDGE['chicken'] = deque()
        FRIDGE['eggs'] = deque()
        FRIDGE['potato'] = deque()
        FRIDGE['radish'] = deque()
        FRIDGE['garlic'] = deque()
        FRIDGE['lettuce'] = deque()
        FRIDGE['tomato'] = deque()
    
    # os.system('cls||clear')
    
    return 1

while AskForInput():
    pass