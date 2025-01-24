# %%
import pandas as pd
import numpy as np
from ast import literal_eval
import spacy 


# # %%
# df1 = pd.read_csv(r'RAW_recipes.csv')
# df2 = pd.read_csv(r'RAW_interactions.csv')
nlp_NER = spacy.load(r'Query_sys\NER\output\model-best')

# # %%
# rating = df2.groupby('recipe_id')['rating'].mean()
# rating = pd.DataFrame(rating)
# rating.index.names = ['id']
# rating

# # %%
# df = df1.merge(rating, on= 'id')
# df.nutrition = df.nutrition.apply(literal_eval)
# df[['calories',
#     'total_fat (%DV)',
#     'sugar (%DV)',
#     'sodium (%DV)',
#     'protein (%DV)',
#     'saturated_fat (%DV)',
#     'total_carbohydrate (%DV)']] = list(n for n in df.nutrition)

# df = df.drop(columns= ['contributor_id', 'submitted', 'tags', 'description', 'nutrition'])
# df = df[df.name.notnull()]
# df = df.sort_values(by= 'rating', ascending= False)

# %%
def extract(text):
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

# compo = extract('What is a filling breakfast recipe with eggs, sausage, and potato?')
# compo

# %%
def to_query(df_, component):
    ingredients, style = component.values()
    filtered_df = df_.copy()
    for ingredient in ingredients:
        filtered_df = filtered_df[filtered_df.ingredients.str.contains(f'{ingredient}')]

    for s in style:
        filtered_df = filtered_df[filtered_df.name.str.contains(f'{s}')]

    return filtered_df


# to_query(df, compo)


