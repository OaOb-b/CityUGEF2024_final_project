# recipe_app.py
import tkinter as tk
from tkinter import messagebox

class RecipeApp:
    def __init__(self, root, yolo_function, recommendation_function):
        self.root = root
        self.root.geometry("414x736")
        self.root.wm_resizable(False, False)

        self.yolo_function = yolo_function
        self.recommendation_function = recommendation_function

        self.create_widgets()

    def create_widgets(self):
        # Button for object detection
        self.detect_button = tk.Button(self.root, text="ENTER THE OBJECT DETECTION", command=self.run_yolo, bg="skyblue", width=30, height=5)
        self.detect_button.pack()

        # Label for ingredient input
        self.ingredient_label = tk.Label(self.root, text="Do you have other ingredients? Please enter below", font=("Arial", 16))
        self.ingredient_label.pack(pady=20)

        # Entry for ingredients
        self.entry = tk.Entry(self.root, font=("Arial", 14), width=40)
        self.entry.pack(pady=(10, 20))

        # Submit button for ingredients
        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit, font=("Arial", 14), bg="#4CAF50", fg="black")
        self.submit_button.pack(pady=20)

        # Button for recipe recommendation
        self.recipe_button = tk.Button(self.root, text="ENTER THE RECIPE RECOMMENDATION", command=self.run_res, bg="skyblue", width=30, height=5)
        self.recipe_button.pack()

        # Label for disease selection
        self.disease_label = tk.Label(self.root, text="Do you have other diseases? Please select below", font=("Arial", 16))
        self.disease_label.pack(pady=20)

        # Listbox for disease selection
        self.listbox = tk.Listbox(self.root, font=("Arial", 14), height=7, selectmode=tk.MULTIPLE)
        self.listbox.pack(pady=20)

        # List of diseases
        items = ["heart disease", "diabetes", "obesity", "high cholesterol", "hypertension", "chronic kidney disease", "bowel cancer"]
        for item in items:
            self.listbox.insert(tk.END, item)

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_submit(self):
        user_input = self.entry.get()
        messagebox.showinfo("Information", "Your information has been saved")
        return user_input

    def on_select(self, event=None):
        selected_indices = self.listbox.curselection()
        selected_values = [self.listbox.get(i) for i in selected_indices]
        print(f"You selected: {', '.join(selected_values)}")

    def run_yolo(self):
        if self.yolo_function:
            self.yolo_function()
        else:
            print("YOLO function is not defined.")

    def run_res(self):
        if self.recommendation_function:
            self.recommendation_function()
        else:
            print("Recommendation function is not defined.")