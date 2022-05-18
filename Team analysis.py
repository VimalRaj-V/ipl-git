# -*- coding: utf-8 -*-
"""
Created on Thu May 20 20:14:44 2021

Author: Vimal Raj V
Title: Pandas(Python and Data analysis)
Institution: Indian Institute of Technology, Madras
"""

import pandas as pd
import numpy as np
import csv

def runRate (runs,balls):
    return (round(runs/balls*6,2))

def economy (runs,balls):
    return (round((runs/balls)*6,2))

data = pd.read_csv("ipl_all_matches.csv")
data_csv = data.copy()

data_csv["innings"] = data_csv["innings"].astype('category')
data_csv['ball'] = data_csv['ball'].astype('category')
data_csv["batting_team"] = data_csv["batting_team"].astype('category')
data_csv["bowling_team"] = data_csv["bowling_team"].astype('category')


Team = np.unique(data_csv["batting_team"])
score = {}
for team in Team :
        score[team] = {"total_runs": 0 , "run_rate":0,'balls_faced':0,"sixes": 0, "boundaries": 0,
                       'runs_conceded':0,'wickets':0,'balls_bowled':0,'economy':0}

i = 0
for run in data_csv['runs_off_bat']:
    team1 = data_csv ['batting_team'][i]
    team2 = data_csv ['bowling_team'][i]
    ball = (float(data_csv['ball'][i])*10%10)
    if (ball<= 6):
        score[team1]['balls_faced'] += 1
    if (ball <= 6):
        score[team2]['balls_bowled'] += 1
    if type(data_csv ['wicket_type'][i]) == str:
        score [team2]['wickets'] += 1 
    runs = (data_csv['runs_off_bat'][i] + data_csv['extras'][i])
    score [team1]['total_runs'] += runs
    score [team2]['runs_conceded'] += runs
    if (run == 6):
        score [team1]['sixes'] += 1
    elif (run == 4):
        score [team1]['boundaries'] += 1
    i += 1  
    
for team in Team:
    score[team]['run_rate'] = runRate(score[team]['total_runs'],score[team]['balls_faced'])
    score[team]['economy'] = economy(score[team]['runs_conceded'],score[team]['balls_bowled'])

filename = "Teams_processed.csv"
fields = ['Index','team_name',"total_runs",'balls_faced','run_rate',"sixes", "boundaries",
                       'runs_conceded','wickets','balls_bowled','economy'] 


# writing to csv file 
with open(filename,'w',newline = '') as csvfile: 
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields)
    # writing the data rows 
    i = 1
    for team in Team:
        detail =  [i,team,score[team]["total_runs"],score[team]['balls_faced'],score[team]['run_rate'],
                   score[team]["sixes"], score[team]["boundaries"],score[team]['runs_conceded'],score[team]['wickets'],
                   score[team]['balls_bowled'],score[team]['economy']]
        csvwriter.writerow(detail)
        i += 1