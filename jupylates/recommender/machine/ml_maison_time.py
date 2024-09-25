import pandas as pd
import numpy as np
import warnings
import joblib
import os
import math


def features_one_user(df, exo , liste_activities,actual_theme):
    # path 
    target_directory = os.getcwd()+'/models/'+actual_theme
    
    average_time_diff = joblib.load(target_directory+'/average_time_diff.pkl')    
    
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
            TR.append(v*num_success/num_attempts * (time-w))
        else:
            TR.append(-num_attempts/4)
    return TR  

    
def Quality_function(prob_of_success, avg_prob_success, exo ,liste_activities,actual_theme):
    # path 
    target_directory = os.getcwd()+'/models/'+actual_theme
    
    quality = prob_of_success[liste_activities.index(exo)]/avg_prob_success[liste_activities.index(exo)]
    if quality >= 1.15:
        return "Good"
    elif quality >= 0.85:
        return "Normal"
    else:
        return "Bad"
    
def predict_success_student(df,liste_activities,actual_theme):
    # path 
    target_directory = os.getcwd()+'/models/'
    
    prob_of_success = []
    df_prob = pd.DataFrame({"student": [0]})
    # Make prediction using the model from models that is made for exercise x (modelx)
    for exercice in range(1, len(liste_activities)+1):
        model = joblib.load(target_directory+liste_activities[exercice-1][:-2]+'pkl')
        
        probability = model.predict_proba(df.drop('TR'+str(exercice), axis=1))
        prob_of_success.append(probability[0][1])
        df_prob.insert(exercice, "Exercice "+str(exercice), probability[0][1])

    return df_prob, prob_of_success




# %%


def maison_time(liste_activities,actual_theme):  
    # path
    target_directory = os.getcwd()+'/models/'+actual_theme
    
    ignore_warnings = warnings.filterwarnings('ignore')        
    avg_prob_success = joblib.load(target_directory+'/avg_prob_success.pkl')
    
    lrs = pd.read_json('.lrs.json',lines= True) 
    lrs['time'] = pd.to_datetime(lrs['time'], format='%Y-%m-%d-%H%M%S')

    # keep last tries of each exercices
    histo = pd.DataFrame()
    for ex in lrs.activity.unique():
        data = lrs.loc[lrs.activity == ex]
        nan = data.loc[np.isnan(data.success)]
        if  len( list(nan.time) ) == 0 :
            pass
        elif len( list(nan.time) ) == 1 :
            time = list(nan.time)[0]
            data = data.loc[data.time>=time] 
        else :
            countor = 1
            time = list(nan.time)[-countor]
            while len(list(data.loc[data.time>=time]["success"])) == 1:
                countor += 1
                time = list(nan.time)[-countor]
            data = data.loc[data.time>=time] 
        histo = pd.concat([histo,data])
    lrs = histo.sort_values(by='time')

    #print(lrs)
    lrs['time'] = lrs['time'].diff().fillna(pd.Timedelta(seconds=0))
    lrs['time'] = lrs['time'].dt.total_seconds()
    
    lrs = lrs.loc[lrs.action == "execute"]
    lrs = lrs.loc[lrs.activity.isin(liste_activities)]

    #### tries ####
    activities = list(lrs.activity)
    historique = list(lrs.activity.drop_duplicates())
    
    count = np.zeros(len(historique))
    tentative = np.zeros(len(activities))

    for ind,ex in enumerate(activities):
        count[historique.index(ex)] += 1
        tentative[ind] = count[historique.index(ex)]
    
        user_data = pd.DataFrame({
            'activity': [list(range(1,len(liste_activities)+1))[liste_activities.index(x)] for x in activities],
            'success': lrs.success,
            'Tentative': tentative,
            'time': lrs.time
        })
    # add student id column to the dataframe
    user_data['student'] = 0 # student id 
    first_column = user_data.pop('student') 
    
    user_data.insert(0, 'student', first_column)
    
    last_exercise = user_data['activity'].iloc[-1]
    
    # create dataframe of new input
    df_user = user_data
    
    # Sort by activity 
    df_user = df_user.sort_values(by='activity')
    
    # Sum times for each tentatives with the previous ones
    df_temp = pd.DataFrame({"student": [0]}, index=[0])
    
    for i in range(len(liste_activities)):
        if df_user.loc[df_user.activity == i+1].size == 0:
            df_temp.insert(i+1,"TR"+str(i+1), -1.0)
        else:
            df_temp.insert(i+1,"TR"+str(i+1), features_one_user(df_user, i+1,liste_activities,actual_theme))
    
    df_prob, prob_of_success = predict_success_student(df_temp,liste_activities,actual_theme)

    if histo["student"].size == 0:
        next_exercise = liste_activities[0]
        return next_exercise
    else:
        yes = 0
        prob_max = 0
        for i in range(len(liste_activities)):
            if i+1 not in df_user['activity'].unique():
                if (prob_of_success[i] > prob_max) :
                    prob_max = prob_of_success[i]
                    next_exercise = liste_activities[i]
                    yes = 1
        if yes == 0:
            if last_exercise > 0:
                next_exercise = liste_activities[last_exercise-1]
            else :
                next_exercise = liste_activities[last_exercise]

    quality = Quality_function(prob_of_success, avg_prob_success, next_exercise, liste_activities,actual_theme)
    if quality == "Good":
        # Recommend the next exercise (most correlated exercise) of those he/she has not attempted
        #if next_exercise == liste_activities[last_exercise-1]:
        #    next_exercise = None
        #    return next_exercise
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
                    next_exercise = liste_activities[i-1]
                #else:                                          # useless
                #    next_exercise = last_exercise
        return next_exercise



