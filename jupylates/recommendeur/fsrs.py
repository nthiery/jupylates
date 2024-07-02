from .models import *
import math
from datetime import timezone , date
import pandas as pd
import warnings
import numpy as np
import pytz


class FSRS:
    p: Parameters
    DECAY: float
    FACTOR: float

    def __init__(self) -> None:
        self.p = Parameters()
        self.DECAY = -0.5
        self.FACTOR = 0.9 ** (1 / self.DECAY) - 1

    def repeat(self, card: Card, now: datetime) -> dict[int, SchedulingInfo]:

        #if (now.tzinfo is None) or (now.tzinfo != timezone.utc):
        #    raise ValueError("datetime must be timezone-aware and set to UTC")

        card = copy.deepcopy(card)
        if card.state == State.New:
            card.elapsed_days = 0
        else:
            card.elapsed_days = (now - card.last_review).days
        card.last_review = now
        card.reps += 1
        s = SchedulingCards(card)
        s.update_state(card.state)

        if card.state == State.New:
            self.init_ds(s)

            s.again.due = now + timedelta(minutes=1)
            s.hard.due = now + timedelta(minutes=5)
            s.good.due = now + timedelta(minutes=10)
            easy_interval = self.next_interval(s.easy.stability)
            s.easy.scheduled_days = easy_interval
            s.easy.due = now + timedelta(days=easy_interval)
        elif card.state == State.Learning or card.state == State.Relearning:
            hard_interval = 0
            good_interval = self.next_interval(s.good.stability)
            easy_interval = max(self.next_interval(s.easy.stability), good_interval + 1)

            s.schedule(now, hard_interval, good_interval, easy_interval)
        elif card.state == State.Review:
            interval = card.elapsed_days
            last_d = card.difficulty
            last_s = card.stability
            retrievability = self.forgetting_curve(interval, last_s)
            self.next_ds(s, last_d, last_s, retrievability)

            hard_interval = self.next_interval(s.hard.stability)
            good_interval = self.next_interval(s.good.stability)
            hard_interval = min(hard_interval, good_interval)
            good_interval = max(good_interval, hard_interval + 1)
            easy_interval = max(self.next_interval(s.easy.stability), good_interval + 1)
            s.schedule(now, hard_interval, good_interval, easy_interval)
        return s.record_log(card, now)

    def init_ds(self, s: SchedulingCards) -> None:
        s.again.difficulty = self.init_difficulty(Rating.Again)
        s.again.stability = self.init_stability(Rating.Again)
        s.hard.difficulty = self.init_difficulty(Rating.Hard)
        s.hard.stability = self.init_stability(Rating.Hard)
        s.good.difficulty = self.init_difficulty(Rating.Good)
        s.good.stability = self.init_stability(Rating.Good)
        s.easy.difficulty = self.init_difficulty(Rating.Easy)
        s.easy.stability = self.init_stability(Rating.Easy)

    def next_ds(
        self, s: SchedulingCards, last_d: float, last_s: float, retrievability: float
    ):
        s.again.difficulty = self.next_difficulty(last_d, Rating.Again)
        s.again.stability = self.next_forget_stability(last_d, last_s, retrievability)
        s.hard.difficulty = self.next_difficulty(last_d, Rating.Hard)
        s.hard.stability = self.next_recall_stability(
            last_d, last_s, retrievability, Rating.Hard
        )
        s.good.difficulty = self.next_difficulty(last_d, Rating.Good)
        s.good.stability = self.next_recall_stability(
            last_d, last_s, retrievability, Rating.Good
        )
        s.easy.difficulty = self.next_difficulty(last_d, Rating.Easy)
        s.easy.stability = self.next_recall_stability(
            last_d, last_s, retrievability, Rating.Easy
        )

    def init_stability(self, r: int) -> float:
        return max(self.p.w[r - 1], 0.1)

    def init_difficulty(self, r: int) -> float:
        return min(max(self.p.w[4] - self.p.w[5] * (r - 3), 1), 10)

    def forgetting_curve(self, elapsed_days: int, stability: float) -> float:
        return (1 + self.FACTOR * elapsed_days / stability) ** self.DECAY

    def next_interval(self, s: float) -> int:
        new_interval = (
            s / self.FACTOR * (self.p.request_retention ** (1 / self.DECAY) - 1)
        )
        return min(max(round(new_interval), 1), self.p.maximum_interval)

    def next_difficulty(self, d: float, r: int) -> float:
        next_d = d - self.p.w[6] * (r - 3)
        return min(max(self.mean_reversion(self.p.w[4], next_d), 1), 10)

    def mean_reversion(self, init: float, current: float) -> float:
        return self.p.w[7] * init + (1 - self.p.w[7]) * current

    def next_recall_stability(self, d: float, s: float, r: float, rating: int) -> float:
        hard_penalty = self.p.w[15] if rating == Rating.Hard else 1
        easy_bonus = self.p.w[16] if rating == Rating.Easy else 1
        return s * (
            1
            + math.exp(self.p.w[8])
            * (11 - d)
            * math.pow(s, -self.p.w[9])
            * (math.exp((1 - r) * self.p.w[10]) - 1)
            * hard_penalty
            * easy_bonus
        )

    def next_forget_stability(self, d: float, s: float, r: float) -> float:
        return (
            self.p.w[11]
            * math.pow(d, -self.p.w[12])
            * (math.pow(s + 1, self.p.w[13]) - 1)
            * math.exp((1 - r) * self.p.w[14])
        )


def rec_fsrs(activities):
    #supprime les warnings
    ignore_warnings = warnings.filterwarnings('ignore')
    
    #importation du json de l'élève
    lrs = pd.read_json('.lrs.json',lines= True) 
    
    #liste des exercices faient par l'élève
    lrs_activities = lrs.activity.unique()
    
    #liste des exercices faient par l'élève qui sont dans le thème
    liste_activities_done = [x for x in lrs_activities if x in activities]
    
    ########################### CONVERSION TEMPS/DATES ####################
    #conversion du temps en format Year-month-days-Hours:minutes:secondes
    lrs['time'] = pd.to_datetime(lrs['time'], format='%Y-%m-%d-%H%M%S')
    lrs["date"] = lrs['time'].dt.date
    
    # futur dataframe de sortie
    output = pd.DataFrame(index=liste_activities_done)
    
    # pour utiliser les class FSRS
    f = FSRS()

    ########################### Succès/tentatives/Temps moyen  ####################

    for ex in liste_activities_done:
        card = Card()
        data = lrs.loc[lrs.activity == ex]
        dates = data.loc[data.action == "execute"]["date"].unique()
        for specific_date in dates:
            last_time = max(data.loc[data.action == "execute"]["time"])
            events_jour = data[data['date'] == specific_date]
                        
            events_succ = events_jour.loc[(events_jour.action == "view") | (events_jour.success == 1)]
            events_succ['time_diff'] = events_succ['time'].diff().fillna(pd.Timedelta(seconds=0))
            events_succ['time_diff'] = events_succ['time_diff'].dt.total_seconds()
            events_succ = events_succ.loc[events_succ.success == 1]
  
    ########################### Quality Again/Hard/Good/Easy ###########################
            
            events_execute = events_jour.loc[events_jour.action == 'execute']

            j = 0
            for i in range(events_execute['action'].size):
                scheduling_cards = f.repeat(card, events_execute.iloc[i].time)
                if events_execute.iloc[i].success == 0 :
                    card = scheduling_cards[Rating.Again].card
                else :
                    if events_succ.iloc[j]['time_diff'] > 120:     # exercice difficile si réussit en + de 120 secondes
                        card = scheduling_cards[Rating.Hard].card
                    elif events_succ.iloc[j]['time_diff'] > 30:    # exercice Good si réussit en ]30,120] secondes
                        card = scheduling_cards[Rating.Good].card
                    else :                                         # exercice Easy si réussit en - de 30 secondes
                        card = scheduling_cards[Rating.Hard].card
                    j += 1
                
            output.loc[ex,"previous full"] = last_time
            output.loc[ex,"previous date"] = last_time.date()
            output.loc[ex,"next full"] = card.due
            output.loc[ex,"next date"] = card.due.date()
            
    ########################### Dataframe Sortie + recommendeur ###########################
    
    output2 = output.loc[output['next date'] <= date.today()]
    ####debug###
    #print(output)
    print(output[['previous full', 'next full']])
    ####debug###
        
    if output2.size != 0: 
        rec =  output2.sort_values(by=['next full'],ascending=True).index.to_list()[0] 
    else:
        rec =  output.sort_values(by=['next full'],ascending=True).index.to_list()[0] 
    return rec
