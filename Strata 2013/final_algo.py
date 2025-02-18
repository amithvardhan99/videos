import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import sqlite3
from gensim.utils import *
import spacy
import re
from retrieve_articles_from_api import *

import nltk
nltk.download("all")

nlp = spacy.load("en_core_web_sm")

import warnings
warnings.filterwarnings("ignore")

import random
from faker import Faker

from retrieve_database import *
from recommend_articles import *
from retrieve_top_categories import *
from select_categories_interested import *
from react_to_articles import *
from compare_scores import *
from get_reactions import *

uwc = pd.read_csv("C:\\Users\\amith\\Documents\\GitHub\\AI_repo\\personalisation\\New_Code_2\\users_with_categories.csv")

df, df_sub = retrieve_database()
dfp = retrieve_articles_from_api(df)
df = pd.concat([df,dfp],axis=0).reset_index(drop=True)
list_of_categories = np.unique(df["Category"].values)


user_reactions = pd.read_csv("C:\\Users\\amith\\Documents\\GitHub\\AI_repo\\personalisation\\New_Code_2\\user_reactions_initial.csv")
user_iterations = pd.read_csv("C:\\Users\\amith\\Documents\\GitHub\\AI_repo\\personalisation\\New_Code_2\\user_iterations_initial.csv")

user_id = uwc["user_id"].values
n = 500
"""
df, df_sub = retrieve_database()
list_of_categories = np.unique(df["Category"].values)
"""

for i in range(n):
    chosen_user_id = np.random.choice(user_id)
    user_chosen_category_1 = []
    user_chosen_category = []
    user_chosen_category_1.append(uwc[uwc["user_id"]==chosen_user_id]["category_1"].values[0])
    user_chosen_category_1.append(uwc[uwc["user_id"]==chosen_user_id]["category_2"].values[0])
    user_chosen_category_1.append(uwc[uwc["user_id"]==chosen_user_id]["category_3"].values[0])
    user_chosen_category_1.append(uwc[uwc["user_id"]==chosen_user_id]["category_4"].values[0])
    for j in user_chosen_category_1:
        if str(j) != "nan":
            user_chosen_category.append(j)
    ctc = 0
    df_fin = df.copy()
    if user_iterations.loc[chosen_user_id-1,"iterations"] == 0:
        top_categories = user_chosen_category
    else:
        inde = user_reactions[user_reactions["user_id"] == chosen_user_id].index[0]
        top_categories = compare_scores(user_reactions.loc[inde,"business_score"],user_reactions.loc[inde,"entertainment_score"],user_reactions.loc[inde,"politics_score"],user_reactions.loc[inde,"sports_score"],user_reactions.loc[inde,"technology_score"])
    df_fin, top_categories = get_reactions(df,top_categories)
    ind = user_reactions[user_reactions["user_id"] == chosen_user_id].index[0]
    for j in df_fin["Article Id"].values:
        interactions_1 = df_fin[df_fin["Article Id"]==j][["like","save","magic","share"]].values[0]
        interactions = ""
        for k in interactions_1:
            interactions += str(k)
        user_reactions.loc[ind,"article "+str(j)] = str(interactions)
    politics_score = df_fin["overall_score"][df_fin["Category"]=="Politics"].sum()
    entertainment_score = df_fin["overall_score"][df_fin["Category"]=="Entertainment"].sum()
    sports_score = df_fin["overall_score"][df_fin["Category"]=="Sports"].sum()
    business_score = df_fin["overall_score"][df_fin["Category"]=="Business"].sum()
    technology_score = df_fin["overall_score"][df_fin["Category"]=="Technology"].sum()
    user_reactions.loc[ind,"politics_score"] += politics_score
    user_reactions.loc[ind,"entertainment_score"] += entertainment_score
    user_reactions.loc[ind,"sports_score"] += sports_score
    user_reactions.loc[ind,"business_score"] += business_score
    user_reactions.loc[ind,"technology_score"] += technology_score
    user_iterations.loc[chosen_user_id-1,"iterations"] += 1
    print(i+1)
user_reactions["politics_score"] = np.round(user_reactions["politics_score"],1)
user_reactions["entertainment_score"] = np.round(user_reactions["entertainment_score"],1)
user_reactions["sports_score"] = np.round(user_reactions["sports_score"],1)
user_reactions["business_score"] = np.round(user_reactions["business_score"],1)
user_reactions["technology_score"] = np.round(user_reactions["technology_score"],1)
user_reactions["overall_score"] = np.round(user_reactions[["politics_score", "entertainment_score", "sports_score", "business_score","technology_score"]].sum(axis=1),1)

user_reactions.to_csv("C:\\Users\\amith\\Documents\\GitHub\\AI_repo\\personalisation\\New_Code_2\\user_reactions_final.csv",index=False)
user_iterations.to_csv("C:\\Users\\amith\\Documents\\GitHub\\AI_repo\\personalisation\\New_Code_2\\user_iterations_final.csv",index=False)