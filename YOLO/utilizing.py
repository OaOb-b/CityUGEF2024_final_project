from ultralytics import YOLO

model = YOLO('/YOLO/model/model.pt')  #change the path if needed
classes = set()
results = model(source=0, show= True, conf= 0.4, save= True)
#results = model(source= 1, stream= True)
#for r in results:
#    boxes = r.boxes.cpu().numpy()
#    for i in boxes.cls:
#        classes.add(i)

print(set(classes))