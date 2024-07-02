#!/usr/bin/env python
# coding: utf-8
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-autoscroll,-collapsed,-scrolled,-trusted,-ExecuteTime,-jp-MarkdownHeadingCollapsed
#     notebook_metadata_filter: kernelspec,jupytext,exports,math,rise,semantic,-jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# PINGU 
# %%


import pandas as pd
import numpy as np
import warnings
import joblib
import os
import math


def Features_one_user(df, exo):
    average_time_diff = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/average_time_diff_time.pkl')    
    liste_activities = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/liste_activities.pkl')
    TR =[]
    num_success = 0
    num_attempts = df.loc[df.activity == exo]["Tentative"].max()
    # Handle NaN values
    if np.isnan(num_attempts):
        TR.append(-1.0)
    else:
        if 1 in df.loc[df.activity == exo]["success"].values:
            if 1 in df.loc[df.activity == exo]["success"].values:
                num_success += df.loc[df.activity == exo]["success"].sum()
            # Size of successful attempts
            v = df.loc[df.activity == exo].loc[df.success == 1].shape[0]
            time = math.exp(-0.1 *df.loc[df.activity == exo].loc[df.success == 1]["time"].mean() /average_time_diff.loc[liste_activities[exo-1]].values[0])
            w = 2
            TR.append(v*num_success/num_attempts * time)
        else:
            TR.append(-num_attempts/4)
    return TR

def Quality_function(prob_of_success, avg_prob_success, exo):
    liste_activities = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/liste_activities.pkl')
    quality = prob_of_success[liste_activities.index(exo)]/avg_prob_success[liste_activities.index(exo)]
    if quality >= 1.15:
        return "Good"
    elif quality >= 0.85:
        return "Normal"
    else:
        return "Bad"
    
def predict_success_student(df):
    liste_activities = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/liste_activities.pkl')
    prob_of_success = []
    df_prob = pd.DataFrame({"student": [0]})
    # Make prediction using the model from models that is made for exercise x (modelx)
    for exercice in range(1, len(liste_activities)+1):
        model = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/LogisticRegressionModelsBruts/model'+str(exercice)+'.pkl')
        
        probability = model.predict_proba(df.drop('TR'+str(exercice), axis=1))
        prob_of_success.append(probability[0][1])
        df_prob.insert(exercice, "Exercice "+str(exercice), probability[0][1])

    return df_prob, prob_of_success




# %%


def maison_time(liste_exo):  
    ignore_warnings = warnings.filterwarnings('ignore')        
    df               = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/df.pkl') 
    win_matrix       = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/win_matrix.pkl')
    win_matrix_df    = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/win_matrix_df.pkl')
    avg_prob_success = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/avg_prob_success.pkl')
    liste_activities = joblib.load('/home/mambauser/jupylates/jupylates/recommendeur/liste_activities.pkl')
    
    lrs = pd.read_json('.lrs.json',lines= True) 
    lrs['time'] = pd.to_datetime(lrs['time'], format='%Y-%m-%d-%H%M%S')
    
    #events_succ = events_jour.loc[(events_jour.action == "view") | (events_jour.success == 1)]
    lrs['time'] = lrs['time'].diff().fillna(pd.Timedelta(seconds=0))
    lrs['time'] = lrs['time'].dt.total_seconds()
    
    lrs = lrs.loc[lrs.action == "execute"]
    
    #### tentative ####
    activities = list(lrs.activity)
    historique = list(lrs.activity.drop_duplicates())
    
    count = np.zeros(len(historique))
    tentative = np.zeros(len(activities))
    for ind,ex in enumerate(activities):
        count[historique.index(ex)] += 1
        tentative[ind] = count[historique.index(ex)]
    
        user_data = pd.DataFrame({
            'activity': [list(range(1,16))[liste_activities.index(x)] for x in activities],
            'success': lrs.success,
            'Tentative': tentative,
            'time': lrs.time
        })
    # add student id column to the dataframe
    user_data['student'] = 0 # student id 
    first_column = user_data.pop('student') 
    
    user_data.insert(0, 'student', first_column)
    
    last_exercise = user_data['activity'].iloc[-1]
    # read previous histo  

    # Vérifier si le fichier existe
    if not os.path.exists("/home/mambauser/jupylates/jupylates/recommendeur/histo.csv"):
        # Créer un DataFrame vide avec des colonnes par défaut
        histo = pd.DataFrame(columns = ['student','activity','success','Tentative','time'] )
        histo.to_csv("/home/mambauser/jupylates/jupylates/recommendeur/histo.csv")
    
    
    histo = pd.read_csv("/home/mambauser/jupylates/jupylates/recommendeur/histo.csv")
    histo = histo.iloc[: , 1:]
    user_data.to_csv("/home/mambauser/jupylates/jupylates/recommendeur/histo.csv")
    
    # we delete the previous results
    
    
    new = user_data.iloc[ histo['activity'].size: ]
    #print(new)
    for ex in new['activity'].unique():
        histo = histo.drop(index = histo.loc[histo.activity == ex].index)  
    
    
    # create dataframe of new input
    df_user = pd.concat([histo,new])
    #print(df_user)
    
    # joblib.dump(df_user, 'df_user2.pkl')
    # df_user= joblib.load('df_user2.pkl')
    
    # Sort by activity 
    df_user = df_user.sort_values(by='activity')
    
    # Sum times for each tentatives with the previous ones
    df_temp = pd.DataFrame({"student": [0]}, index=[0])
    
    for i in range(len(liste_activities)):
        if df_user.loc[df_user.activity == i+1].size == 0:
            df_temp.insert(i+1,"TR"+str(i+1), -1.0)
        else:
            df_temp.insert(i+1,"TR"+str(i+1), Features_one_user(df_user, i+1))
    
    df_prob, prob_of_success = predict_success_student(df_temp)

    if histo["student"].size == 0:
        next_exercise = liste_activities[0]
        return next_exercise
    else:
        yes = 0
        prob_max = 0
        for i in range(len(liste_activities)):
            if i+1 not in df_user['activity'].unique():
                if (prob_of_success[i] > prob_max) and (liste_activities[i] in liste_exo):
                    prob_max = prob_of_success[i]
                    next_exercise = liste_activities[i]
                    yes = 1
        if yes == 0:
            if liste_activities[last_exercise-1] in liste_exo:
                next_exercise = liste_activities[last_exercise-1]
            else:
                next_exercise = liste_activities[last_exercise]

    quality = Quality_function(prob_of_success, avg_prob_success, next_exercise)
    #print(f"Quality of the student: {quality}")
    if quality == "Good":
        print("GOOOOOOOOOOOOOOOOOOpinguOOOOOOOOD")
        # Recommend the next exercise (most correlated exercise) of those he/she has not attempted
        if next_exercise == liste_activities[last_exercise-1]:
            next_exercise = None
            return next_exercise
        return next_exercise
    elif quality == "Normal":
        # Recommend revision and repetition of the last exercise
        next_exercise = liste_activities[last_exercise]
        return next_exercise
    else:
        # Recommend the most correlated exercise of those he/she has attempted
        if len(df_user['activity'].unique()) == 1:
            return liste_activities[last_exercise]
        else:
            # Most probable exercise of the attempted exercises in the theme
            prob_max = 0
            for i in df_user['activity'].unique():
                if prob_of_success[i-1] > prob_max:
                    prob_max = prob_of_success[i-1]
                    next_exercise = liste_exo[i-1]
                #else:                                          # useless
                #    next_exercise = last_exercise
        return next_exercise



