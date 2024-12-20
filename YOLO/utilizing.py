from ultralytics import YOLO
import tkinter

top = tkinter.Tk()
global classes
def run():
    model = YOLO('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/YOLO/model/model.pt')  #change the path if needed (use model.pt)
    classes = set()
    results = model(source=0, show= True, conf= 0.4, save= True)
    print(set(classes))

B = tkinter.Button(top, text ="press me", command = run)
B.pack()
top.mainloop()

#print(set(classes))