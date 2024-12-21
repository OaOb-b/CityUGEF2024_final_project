from ultralytics import YOLO
import tkinter
from tkinter import messagebox
global input
def runYOLO():
    model = YOLO('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/YOLO/model/model.pt')  #change the path if needed (use model.pt)
    classes = set()
    results = model(source=0, show= True, conf= 0.4, save= True)
    print(set(classes))

def runRes():
    messagebox.showinfo("Information", input)
    return ("hi")
     
    
top = tkinter.Tk()

def on_submit():
    user_input = entry.get()
    global input 
    input = user_input
    messagebox.showinfo("Information", f"Your infomation have been saved")
    return user_input

top.geometry("414x736")
top.wm_resizable(False,False)

entry = tkinter.Entry(top, font=("Arial", 14), width=25)
entry.pack(pady=10)

submit_button = tkinter.Button(top, text="Submit", command=on_submit, font=("Arial", 14), bg="#4CAF50", fg="white")
submit_button.pack(pady=20)


A = tkinter.Button(top, text ="ENTER THE RECIPE RECOMMEMDATION", command = runRes , bg = "red")
A.pack()

B = tkinter.Button(top, text ="ENTER THE OBJECT DETECTION", command = runYOLO , bg = "skyblue")
B.pack()

top.mainloop()
