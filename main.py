from ultralytics import YOLO
import tkinter
from tkinter import messagebox
import pandas as pd
import numpy as np
from ast import literal_eval
import spacy 

global input

#Query
df1 = pd.read_csv('/Users/paco/Downloads/Food.com Recipes/RAW_recipes.csv')
df2 = pd.read_csv('/Users/paco/Downloads/Food.com Recipes/RAW_interactions.csv')
nlp_NER = spacy.load('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/Query_sys/NER/output/model-best')
rating = df2.groupby('recipe_id')['rating'].mean()
rating = pd.DataFrame(rating)
rating.index.names = ['id']
df = df1.merge(rating, on= 'id')
df.nutrition = df.nutrition.apply(literal_eval)
df[['calories',
    'total_fat (%DV)',
    'sugar (%DV)',
    'sodium (%DV)',
    'protein (%DV)',
    'saturated_fat (%DV)',
    'total_carbohydrate (%DV)']] = list(n for n in df.nutrition)

df = df.drop(columns= ['contributor_id', 'submitted', 'tags', 'description', 'nutrition'])
df = df[df.name.notnull()]
df = df.sort_values(by= 'rating', ascending= False)
def rizz(text):
    doc = nlp_NER(text)
    component = {'ingredients': [], 'style': []} 
    for ent in doc.ents:
        text = ent.text
        if ent.label_ == 'ingredient':
            if text[-3:] == 'ies':
                text = text.removesuffix('ies')
                text += 'y'
            elif text[-2:] == 'es':
                text = text.removesuffix('es')
            elif text[-1:] == 's':
                text = text.removesuffix('s')
            component['ingredients'].append(text)
            
        elif ent.label_ == 'product':
            component['style'].append(text)
    
    return component

def to_query(df_, component):
    ingredients, style = component.values()
    filtered_df = df_.copy()
    for ingredient in ingredients:
        filtered_df = filtered_df[filtered_df.ingredients.str.contains(f'{ingredient}')]

    return filtered_df

#YOLO
model = YOLO('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/YOLO/model/model.pt')  #change the path if needed (use model.pt)
classes = set()

    
def runYOLO():  
    results = model(source=0, show= True, conf= 0.4, save= True)
    print(set(classes))

def runRes():
    global input
    prom = input
    compo = rizz(prom)
    recipe = to_query(df,compo)
    messagebox.showinfo("Information", recipe[1])

top = tkinter.Tk()

def on_submit():
    user_input = entry.get() 
    global input 
    input = user_input
    messagebox.showinfo("Information", f"Your infomation have been saved")
    #print(input)
    return user_input

top.geometry("414x736")
top.wm_resizable(False,False)

B = tkinter.Button(top, text ="ENTER THE OBJECT DETECTION", command = runYOLO , bg = "skyblue")
B.pack()

entry = tkinter.Entry(top, font=("Arial", 14), width=25)
entry.pack(pady=10)

submit_button = tkinter.Button(top, text="Submit", command=on_submit, font=("Arial", 14), bg="#4CAF50", fg="white")
submit_button.pack(pady=20)

A = tkinter.Button(top, text ="ENTER THE RECIPE RECOMMEMDATION", command = runRes , bg = "skyblue")
A.pack()

top.mainloop()
