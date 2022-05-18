"""
Created on Fri Jun  4 16:31:38 2021

Author: Vimal Raj V
Title: Pandas(Python and Data analysis)
Institution: Indian Institute of Technology, Madras
"""

import pandas as pd
import numpy as np
import csv

def strikeRate (runs,balls):
    if (balls == 0):
        return (0)
    return (round((runs/balls)*100,2))

def economy (runs,balls):
    if balls == 0:
        return (0)
    return (round((runs/balls)*6,2))

def playerCategory(Innings, Matches):
    if Matches == 0:
        return('Batsman')
    elif Innings == 0:
        return('Bowler')
    elif (Innings/Matches) > 1.5:
        return('Batsman')
    elif (Innings/Matches) < 0.5:
        return('Bowler')
    else:
        return ('All rounder')

data_csv = pd.read_csv("ipl_all_matches.csv")

data_csv["innings"] = data_csv["innings"].astype('category')
data_csv['ball'] = data_csv['ball'].astype('category')
data_csv["batting_team"] = data_csv["batting_team"].astype('category')
data_csv["bowling_team"] = data_csv["bowling_team"].astype('category')

data_csv.insert(9,'batsmen_score',0)
data_csv.insert(10,'balls_faced',0)
data_csv.insert(11,'balls_faced_as_NS',0)
data_csv.insert(12,'strike_rate',0.0)
data_csv.insert(15,'balls_bowled',0)
data_csv.insert(16,'runs_conceded',0)
data_csv.insert(17,'economy',0.0)
data_csv.insert(18,'wickets',0)
data_csv.insert(19,'Player_type','')

batsmen = set(np.unique(data_csv["striker"]))
bowler = set(np.unique(data_csv['bowler']))
players = batsmen | bowler
stats = {}
stat1 = {}
stat2 = {}
wicket_type = ['bowled','caught','stumped','lbw']

for player in players:
    stats[player] = {'innings':0,'team':"",'runs':0,'balls_faced(s)':0,'balls_faced(ns)':0,'strike_rate':0,
                     'Fours':0,'sixes':0,'highest_score':0,'hs_vs':'','hs_sr':0,'not_outs':0,
                     'matches':0,'balls_bowled':0,'overs':0,'runs_conceded':0,'wickets':0,'economy':0 }

for i in range(len(data_csv['match_id'])):
    ID = data_csv['match_id'][i]
    s = data_csv['striker'][i]
    ns = data_csv['non_striker'][i]
    b = data_csv['bowler'][i]
    batTe = data_csv ['batting_team'][i]
    bowTe = data_csv ['bowling_team'][i]
    r = data_csv ['runs_off_bat'][i]
    ball = (float(data_csv['ball'][i])*10%10)
    if s not in stat1:
        stat1 [s] = {}
    if ID not in stat1[s]:
        stat1[s][ID] = [0,0,0,0,batTe,bowTe,0,0]
    if ns not in stat1:
        stat1 [ns] = {}
    if ID not in stat1[ns]:
        stat1[ns][ID] = [0,0,0,0,batTe,bowTe,0,0]
        
    stat1[s][ID][0] += r
    stat1[s][ID][1] += 1
    stat1[ns][ID][2] += 1
    if (r == 4):
        stat1[s][ID][6] += 1
    if (r == 6):
        stat1[s][ID][7] += 1
    if (data_csv['player_dismissed'][i] == s):
        stat1[s][ID][3] += 1
    if (data_csv['player_dismissed'][i] == ns):
        stat1[ns][ID][3] += 1
    if b not in stat2:
        stat2[b] = {}
    if ID not in stat2[b]:
        stat2[b][ID] = [0,0,0,0,0,bowTe,batTe]
    if (ball <= 6):
        stat2[b][ID][0] += 1
        if (ball == 6):
            stat2[b][ID][1] += 1
    stat2[b][ID][2] +=  (r + data_csv['extras'][i])
    if (data_csv['wicket_type'][i] in wicket_type):
        stat2[b][ID][3] += 1

for batsman in stat1:
    for match in stat1[batsman]:
        stats[batsman]['innings'] += 1
        stats[batsman]['team'] = stat1[batsman][match][4]
        stats[batsman]['runs'] += stat1[batsman][match][0]
        stats[batsman]['balls_faced(s)'] += stat1[batsman][match][1]
        stats[batsman]['balls_faced(ns)'] += stat1[batsman][match][2]
        stats[batsman]['not_outs'] += stat1[batsman][match][3]
        stats[batsman]['Fours'] += stat1[batsman][match][6]
        stats[batsman]['sixes'] += stat1[batsman][match][7]
        stats[batsman]['strike_rate'] += strikeRate(stat1[batsman][match][0] , stat1[batsman][match][1])
        if (stats[batsman]['highest_score'] <= stat1[batsman][match][0]):
            stats[batsman]['highest_score'] = stat1[batsman][match][0]
            stats[batsman]['hs_vs'] = stat1[batsman][match][5]
            stats[batsman]['hs_sr'] = strikeRate(stat1[batsman][match][0] , stat1[batsman][match][1])
    stats[batsman]['strike_rate'] /= stats[batsman]['innings']
    stats[batsman]['not_outs'] = stats[batsman]['innings'] - stats[batsman]['not_outs']

for bowl in stat2:
    for match in stat2[bowl]:
        stats[bowl]['matches'] += 1
        stats[bowl]['team'] = stat2[bowl][match][5]
        stats[bowl]['balls_bowled'] += stat2[bowl][match][0]
        stats[bowl]['overs'] += stat2[bowl][match][1]
        stats[bowl]['wickets'] += stat2[bowl][match][3]
        stats[bowl]['runs_conceded'] += stat2[bowl][match][2]
        stats[bowl]['economy'] += economy (stats[bowl]['runs_conceded'],stats[bowl]['balls_bowled'])
    stats[bowl]['economy'] /= stats[bowl]['matches']

filename = "ipl_record_players.csv"
fields = ['Index','Name','Innings', 'Team','batsmen_score', 'balls_faced','balls_faced_as_NS', 'strike_rate','fours','sixes','Not_outs',
          'Highest_score','Hs_vs','Hs_SR','matches','balls_bowled','Overs', 'runs_conceded','Wickets', 'economy', 'player_Category'] 

# writing to csv file 
with open(filename, 'w',newline = '') as csvfile:
    
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields)
    # writing the data rows 
    i = 0
    for name in stats:
        detail = [i,name,stats[name]['innings'],stats[name]['team'],stats[name]['runs'],
                  stats[name]['balls_faced(s)'],stats[name]['balls_faced(ns)'],stats[name]['strike_rate'],stats[name]['Fours'],stats[name]['sixes'],
                  stats[name]['not_outs'],stats[name]['highest_score'],stats[name]['hs_vs'],
                  stats[name]['hs_sr'],stats[name]['matches'],stats[name]['balls_bowled'],
                  stats[name]['overs'],stats[name]['runs_conceded'],stats[name]['wickets'],
                  stats[name]['economy'], playerCategory(stats[name]['innings'], stats[name]['matches'])]
        csvwriter.writerow(detail)
        i += 1