import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from ast import literal_eval
import spacy
from ultralytics import YOLO

class RecipeDataset:
    def __init__(self, recipes_path, interactions_path):
        self.df1 = pd.read_csv(recipes_path)
        self.df2 = pd.read_csv(interactions_path)
        self.prepare_data()

    def prepare_data(self):
        rating = self.df2.groupby('recipe_id')['rating'].mean()
        rating = pd.DataFrame(rating)
        rating.index.names = ['id']
        self.df = self.df1.merge(rating, on='id')
        self.df.nutrition = self.df.nutrition.apply(literal_eval)
        self.df[['calories', 'total_fat (%DV)', 'sugar (%DV)', 
                  'sodium (%DV)', 'protein (%DV)', 'saturated_fat (%DV)', 
                  'total_carbohydrate (%DV)']] = list(n for n in self.df.nutrition)
        self.df = self.df.drop(columns=['contributor_id', 'submitted', 
                                          'tags', 'description', 'nutrition'])
        self.df = self.df[self.df.name.notnull()]
        self.df = self.df.sort_values(by='rating', ascending=False)

class RecipeNLP:
    def __init__(self, model_path):
        self.nlp = spacy.load(model_path)

    def extract_components(self, text):
        doc = self.nlp(text)
        component = {'ingredients': [], 'style': []}
        for ent in doc.ents:
            text = ent.text
            if ent.label_ == 'ingredient':
                if text.endswith('ies'):
                    text = text[:-3] + 'y'
                elif text.endswith('es'):
                    text = text[:-2]
                elif text.endswith('s'):
                    text = text[:-1]
                component['ingredients'].append(text)
            elif ent.label_ == 'product':
                component['style'].append(text)
        return component

class YOLOModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def run_detection(self):
        results = self.model(source=0, show=True, conf=0.4, save=True)

class RecipeRecommenderApp:
    def __init__(self, root, dataset, nlp_model, yolo_model):
        self.root = root
        self.dataset = dataset
        self.nlp_model = nlp_model
        self.yolo_model = yolo_model
        self.input_text = ''
        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("414x736")
        self.root.wm_resizable(False, False)

        tk.Button(self.root, text="ENTER THE OBJECT DETECTION", command=self.run_yolo, bg="skyblue", width=30, height=5).pack()
        
        tk.Label(self.root, text="Do you have other ingredients? Please enter below", font=("Arial", 16)).pack(pady=20)
        
        self.entry = tk.Entry(self.root, font=("Arial", 14), width=40)
        self.entry.pack(pady=(10, 20))
        
        tk.Button(self.root, text="Submit", command=self.on_submit, font=("Arial", 14), bg="#4CAF50", fg="black").pack(pady=20)
        
        tk.Button(self.root, text="ENTER THE RECIPE RECOMMENDATION", command=self.run_recommendation, bg="skyblue", width=30, height=5).pack()
        
        tk.Label(self.root, text="Do you have other diseases? Please select below", font=("Arial", 16)).pack(pady=20)
        
        self.listbox = tk.Listbox(self.root, font=("Arial", 14), height=7, selectmode=tk.MULTIPLE)
        self.listbox.pack(pady=20)
        
        items = ["heart disease", "diabetes", "obesity", "high cholesterol", "hypertension", "chronic kidney disease", "bowel cancer"]
        for item in items:
            self.listbox.insert(tk.END, item)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def run_yolo(self):
        self.yolo_model.run_detection()

    def on_submit(self):
        self.input_text = self.entry.get()
        messagebox.showinfo("Information", "Your information has been saved.")

    def run_recommendation(self):
        components = self.nlp_model.extract_components(self.input_text)
        filtered_recipes = self.to_query(components)
        messagebox.showinfo("Information", filtered_recipes.to_string())

    def to_query(self, component):
        ingredients = component['ingredients']
        filtered_df = self.dataset.df.copy()
        for ingredient in ingredients:
            filtered_df = filtered_df[filtered_df.ingredients.str.contains(f'{ingredient}', na=False)]
        return filtered_df

if __name__ == "__main__":
    root = tk.Tk()
    dataset = RecipeDataset('/Users/paco/Downloads/Food.com Recipes/RAW_recipes.csv',
                            '/Users/paco/Downloads/Food.com Recipes/RAW_interactions.csv')
    nlp_model = RecipeNLP('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/Query_sys/NER/output/model-best')
    yolo_model = YOLOModel('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/YOLO/model/model.pt')

    app = RecipeRecommenderApp(root, dataset, nlp_model, yolo_model)
    root.mainloop()