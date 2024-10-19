########### import for recommended exercice
import pandas as pd
import numpy as np
from math import ceil
from datetime import timedelta, date
import warnings


################################# RECOMMENDEUR #################################
def Quality(success, temps):

    eval_try = 2.5 * success
    if eval_try == 0:
        eval_time = 0
    else:
        eval_time = 51 * np.exp(-0.1 * temps)
        if eval_time > 2.5:
            eval_time = 2.5

    return eval_try + eval_time


def efficiency(ef, Quality):
    ef = ef + (0.1 - (5 - Quality) * (0.08 + (5 - Quality) * 0.02))
    if ef < 1.3:
        ef = 1.3
    return ef


def rec_SM2(activities, lrs_url=".lrs.json"):

    ############# LECTURE LRS ################

    # supprime les warnings
    ignore_warnings = warnings.filterwarnings("ignore")

    # importation du json de l'élève
    lrs = pd.read_json(lrs_url, lines=True)
    # liste des exercices faient par l'élève
    lrs_activities = list(
        lrs.loc[lrs.action == "execute"]["activity"].drop_duplicates()
    )
    liste_activities_done = [x for x in lrs_activities if x in activities]

    ########################### CONVERSION TEMPS/DATES ####################

    lrs["time"] = pd.to_datetime(lrs["time"], format="%Y-%m-%d-%H%M%S")
    lrs["date"] = lrs["time"].dt.date

    output = pd.DataFrame(columns=["ef"], index=liste_activities_done)
    output.loc[:, "ef"] = 2.5

    ########################### CALCUL DE EF DES EXERCICES DEPUIS JOURS 0 ####################

    for ex in liste_activities_done:
        data = lrs.loc[lrs.activity == ex]
        dates = data.loc[data.action == "execute"]["date"].drop_duplicates()
        for specific_date in dates:
            events_jour = data[data["date"] == specific_date]

            tentatives = events_jour.loc[events_jour.action == "execute"][
                "action"
            ].size  # !!!!!!!!

            events_succ = events_jour.loc[
                (events_jour.action == "view") | (events_jour.success == 1)
            ]
            events_succ["time_diff"] = (
                events_succ["time"].diff().fillna(pd.Timedelta(seconds=0))
            )
            events_succ["time_diff"] = events_succ["time_diff"].dt.total_seconds()
            events_succ = events_succ.loc[events_succ.success == 1]

            # si l'éléve passe plus de 120 secondes on considere son temps à 120 secondes
            events_succ["time_diff"].loc[events_succ["time_diff"] > 120] = 120

            events_execute = events_jour.loc[events_jour.action == "execute"]
            repetition = 0
            for i in range(events_execute["action"].size):
                if events_execute.iloc[i].success == 0:
                    Qual_ex = Quality(0, 0)
                else:

                    Qual_ex = Quality(1, events_succ.iloc[repetition].time_diff)
                    repetition += 1
                output.loc[ex, "ef"] = efficiency(output.loc[ex, "ef"], Qual_ex)

        output.loc[ex, "Previous Date"] = specific_date

        if Qual_ex < 3:
            interval = 0
            repetition = 0
        else:
            if repetition == 0:
                interval = 1
            elif repetition > 4:
                interval = 6
            else:
                interval = output.loc[ex, "ef"]

        output.loc[ex, "Next Date"] = specific_date + timedelta(days=ceil(interval))

    ###########################                                           ####################

    output2 = output.loc[output["Next Date"] <= date.today()]

    ####debug###
    print(output)
    ####debug###

    if output2.size != 0:
        rec = output2.sort_values(by=["ef"], ascending=True).index.to_list()[0]
    else:
        rec = output.sort_values(by=["ef"], ascending=True).index.to_list()[0]
    return rec
