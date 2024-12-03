from ultralytics import YOLO

model = YOLO(r'CNNs\YOLO\best.pt')
classes = set()
# results = model(source= r"C:\Users\user\Desktop\abc.mp4", show= True, conf= 0.4, save= True)
results = model(source= r"C:\Users\user\Desktop\abc.mp4", stream= True)
for r in results:
    boxes = r.boxes.cpu().numpy()
    for i in boxes.cls:
        classes.add(i)

print(set(classes))