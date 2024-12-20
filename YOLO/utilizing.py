from ultralytics import YOLO
import tkinter


def run():
    model = YOLO('YOLO/model/model.pt')  #change the path if needed (use model.pt)
    classes = set()
    results = model(source=0, show= True, conf= 0.4, save= True)
    print(set(classes))
    
    
top = tkinter.Tk()

top.geometry("414x736")
top.wm_resizable(False,False)

B = tkinter.Button(top, text ="ENTER THE OBJECT DETECTION", command = run , bg = "skyblue")
B.pack()
top.mainloop()

