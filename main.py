import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Frame, Text
import pandas as pd
import shelve
from collections import deque
from YOLO.utilizing import get_stock, ObjectDetection
from Query_sys.df.Query import extract, to_query

# top = tkinter.Tk()



# def on_submit():
#     user_input = entry.get() 
#     global input 
#     input = user_input
#     # Save user input
#     messagebox.showinfo("Information", "Your information has been saved")
#     print(input)
#     return user_input

# top.geometry("414x736")
# top.wm_resizable(False, False)

# def on_select(event=None):
#     # Get the indices of the selected items
#     selected_indices = listbox.curselection()
    
#     # Retrieve the selected values using the indices
#     selected_values = [listbox.get(i) for i in selected_indices]  # Get values for each selected index
    
#     # Print the selected values
#     print(f"You selected: {', '.join(selected_values)}")  # Display selected items

# # B = tkinter.Button(top, text="ENTER THE OBJECT DETECTION", command=runYOLO, bg="skyblue", width=30, height=5)
# # B.pack()

# button_frame = tkinter.Frame(top)
# button_frame.pack(pady=20)

# Create and pack the buttons
# button1 = tkinter.Button(button_frame, text="Button 1", command=ObjectDetection(1)(1))
# button1.pack(side=tkinter.LEFT, padx=5)

# button2 = tkinter.Button(button_frame, text="Button 2", command=ObjectDetection(1)(0))
# button2.pack(side=tkinter.LEFT, padx=5)

# button3 = tkinter.Button(button_frame, text="Button 3", command=get_stock(FRIDGE) )
# button3.pack(side=tkinter.LEFT, padx=5)

# button4 = tkinter.Button(button_frame, text="Button 4", command=print("4"))
# button4.pack(side=tkinter.LEFT, padx=5)

# label = tkinter.Label(top, text="Do you have other ingredients? Please enter below:", font=("Arial", 16))  # Create a label with text
# label.pack(pady=20) 

# entry = tkinter.Entry(top, font=("Arial", 14), width=40)
# entry.pack(pady=(10, 20))

# submit_button = tkinter.Button(top, text="Submit", command=on_submit, font=("Arial", 14), bg="#4CAF50", fg="black")
# submit_button.pack(pady=20)

# # A = tkinter.Button(top, text="ENTER THE RECIPE RECOMMENDATION", command=runRes, bg="skyblue", width=30, height=5)
# # A.pack()

# label = tkinter.Label(top, text="Do you have any diseases? Please select below:", font=("Arial", 16))  # Create a label with text
# label.pack(pady=20) 

# listbox = tkinter.Listbox(top, font=("Arial", 14), height=7, selectmode=tkinter.MULTIPLE)
# listbox.pack(pady=20)

# items = ["heart disease", "diabetes", "obesity", "high cholesterol", "hypertension", "chronic kidney disease", "bowel cancer"]
# for item in items:
#     listbox.insert(tkinter.END, item)
    
# listbox.bind('<<ListboxSelect>>', on_select)

# top.mainloop()

df = pd.read_csv(r'Query_sys\df\Recipes.csv', sep='\t')


print('hello')

mapping = ['Onion',
'beef',
'chicken',
'eggs',
'potato',
'radish',
'garlic',
'lettuce',
'tomato']


FRIDGE = shelve.open(r"YOLO\Fridge\FRIDGE", writeback= True)
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



class root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x1067")
        self.wm_resizable(False, False)

        
        self.mainframe = UI(self)
        self.mainframe.pack(expand= True, fill= tk.BOTH)

        self.mainloop()
        FRIDGE.close()

class UI(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        
        # self.columnconfigure(0, weight= 1)
        # self.rowconfigure(0, weight= 1)
        
        self.create_widgets()

    def create_widgets(self):


        tk.Label(self, text="Cooking Helper", font= ("Arial", 30)).pack(pady= 20)   

        tk.Label(self, text="How may I help you today? :)", font= ("Arial", 16)).pack(pady= 20)   
        
        self.entry = tk.Entry(self, font= ("Arial", 14), width= 50)
        self.entry.pack() 

        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit, font= ("Arial", 14), bg= "#4CAF50", fg= "black")
        self.submit_button.pack(pady= 20)

        button_frame = tk.Frame(self)
        button_frame.pack()
        
        self.check_stock = tk.Button(button_frame, text= "get_stock_from_FRIDGE", command= self.get_stock_from_FRIDGE, font= ("Arial", 14), bg= "#4CAF50", fg= "black")
        self.check_stock.pack(side=tk.LEFT, padx=5)

        self.store = tk.Button(button_frame, text= "Store Ingredient", command= self.stock_it, font= ("Arial", 14), bg= "#4CAF50", fg= "black")
        self.store.pack(side=tk.LEFT, padx=5)

        self.check_stock = tk.Button(button_frame, text= "Consume Ingredient", command= self.consume_it, font= ("Arial", 14), bg= "#4CAF50", fg= "black")
        self.check_stock.pack(side=tk.LEFT, padx=5)


        tk.Label(self, text="Do you have any diseases? Please select them below:", font=("Arial", 16)).pack(pady=20)

        self.listbox = tk.Listbox(self, font=("Arial", 14), height=7, selectmode=tk.MULTIPLE)
        self.listbox.pack(pady=20)

        items = ["heart disease", "diabetes", "obesity", "high cholesterol", "hypertension", "chronic kidney disease", "bowel cancer"]
        for item in items:
            self.listbox.insert(tk.END, item)
            
        self.listbox.bind('<<ListboxSelect>>', self.on_select)



    def on_submit(self):
        user_input = self.entry.get() 
        criteria = extract(user_input)

        if criteria == {}:
            criteria = {'ingredients': list(self.get_stock_from_FRIDGE().keys()),
                        'style': []}
        
        recommend = to_query(df, criteria).head(1)
        print(recommend)

        return recommend

    def get_stock_from_FRIDGE(self):
        return get_stock(FRIDGE)
        

    def stock_it(self):
        ObjectDetection(1)(1)

    def consume_it(self):
        ObjectDetection(1)(0)

    def on_select(self, event=None):
        # Get the indices of the selected items
        selected_indices = self.listbox.curselection()
        
        # Retrieve the selected values using the indices
        selected_values = [self.listbox.get(i) for i in selected_indices]  # Get values for each selected index
        
        # Print the selected values
        print(f"You selected: {', '.join(selected_values)}")  # Display selected items


root()