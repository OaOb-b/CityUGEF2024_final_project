from ultralytics import YOLO
import tkinter
from tkinter import messagebox, Toplevel, Scrollbar, Frame, Text
import pandas as pd
import numpy as np
from ast import literal_eval
import spacy 

global input

# Query
df1 = pd.read_csv('/Users/paco/Downloads/Archive (1)/RAW_recipes.csv')     # Change the path if needed 
df2 = pd.read_csv('/Users/paco/Downloads/Archive (1)/RAW_interactions.csv')    # Change the path if needed 
nlp_NER = spacy.load('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/Query_sys/NER/output/model-best') # Change the path if needed 
rating = df2.groupby('recipe_id')['rating'].mean()
rating = pd.DataFrame(rating)
rating.index.names = ['id']

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
    print(component)
    return component

def to_query(df_, component):
    ingredients, style = component.values()
    filtered_df = df_.copy()
    for ingredient in ingredients:
        filtered_df = filtered_df[filtered_df.ingredients.str.contains(f'{ingredient}')]
    print(filtered_df)
    return filtered_df

# YOLO
model = YOLO('/Users/paco/Documents/GitHub/CityUGEF2024_final_project/YOLO/model/model.pt')  # Change the path if needed (use model.pt)
classes = set()

def runYOLO():  
    results = model(source=0, show=True, conf=0.4, save=True)
    print(set(classes))

def runRes():
    global input
    prom = input

    # Extract components using the NLP model
    compo = rizz(prom)

    # Prepare the DataFrame
    df = df1.merge(rating, on='id')
    df.nutrition = df.nutrition.apply(literal_eval)
    df[['calories', 'total_fat (%DV)', 'sugar (%DV)', 
        'sodium (%DV)', 'protein (%DV)', 
        'saturated_fat (%DV)', 'total_carbohydrate (%DV)']] = list(n for n in df.nutrition)
    
    # Query the DataFrame based on the extracted components
    recipe = to_query(df, compo)

    # Drop unnecessary columns and clean up the DataFrame
    df = df.drop(columns=['contributor_id', 'submitted', 'tags', 'description', 'nutrition'])
    df = df[df.name.notnull()]
    df = df.sort_values(by='rating', ascending=False)

    # Display recipes in a better output window
    display_recipes(recipe)

def display_recipes(recipe):
    # Create a new window for displaying recipes
    recipe_window = Toplevel(top)
    recipe_window.title("Recipe Recommendation")
    recipe_window.geometry("500x600")  # Set the size of the window
    
    recipe_window.configure(bg='black')  # Set a dark background color

    if not recipe.empty:
        row = recipe.iloc[0]  # Select the first recipe
        text_widget = Text(recipe_window, wrap="word", font=("Arial", 12), padx=10, pady=10, bg='black', fg='white')
        text_widget.pack(fill=tkinter.BOTH, expand=True)

        text_widget.insert(tkinter.END, f"Recipe Name: {row['name']}\n")
        text_widget.insert(tkinter.END, f"Ingredients: {row['ingredients']}\n")
        
        # Split the cooking instructions into separate steps and display each step on a new line
        steps = row['steps'].split('\n')
        for step in steps:
            text_widget.insert(tkinter.END, f"{step}\n")
            
    else:
        text_widget = Text(recipe_window, wrap="word", font=("Arial", 12), padx=10, pady=10, bg='black', fg='white')
        text_widget.pack(fill=tkinter.BOTH, expand=True)
        text_widget.insert(tkinter.END, "No recipes found for the given ingredients.")
        
    text_widget.config(state=tkinter.DISABLED)
    
top = tkinter.Tk()

def on_submit():
    user_input = entry.get() 
    global input 
    input = user_input
    # Save user input
    messagebox.showinfo("Information", "Your information has been saved")
    print(input)
    return user_input

top.geometry("414x736")
top.wm_resizable(False, False)

def on_select(event=None):
    # Get the indices of the selected items
    selected_indices = listbox.curselection()
    
    # Retrieve the selected values using the indices
    selected_values = [listbox.get(i) for i in selected_indices]  # Get values for each selected index
    
    # Print the selected values
    print(f"You selected: {', '.join(selected_values)}")  # Display selected items

B = tkinter.Button(top, text="ENTER THE OBJECT DETECTION", command=runYOLO, bg="skyblue", width=30, height=5)
B.pack()

label = tkinter.Label(top, text="Do you have other ingredients? Please enter below:", font=("Arial", 16))  # Create a label with text
label.pack(pady=20) 

entry = tkinter.Entry(top, font=("Arial", 14), width=40)
entry.pack(pady=(10, 20))

submit_button = tkinter.Button(top, text="Submit", command=on_submit, font=("Arial", 14), bg="#4CAF50", fg="black")
submit_button.pack(pady=20)

A = tkinter.Button(top, text="ENTER THE RECIPE RECOMMENDATION", command=runRes, bg="skyblue", width=30, height=5)
A.pack()

label = tkinter.Label(top, text="Do you have any diseases? Please select below:", font=("Arial", 16))  # Create a label with text
label.pack(pady=20) 

listbox = tkinter.Listbox(top, font=("Arial", 14), height=7, selectmode=tkinter.MULTIPLE)
listbox.pack(pady=20)

items = ["heart disease", "diabetes", "obesity", "high cholesterol", "hypertension", "chronic kidney disease", "bowel cancer"]
for item in items:
    listbox.insert(tkinter.END, item)
    
listbox.bind('<<ListboxSelect>>', on_select)

top.mainloop()