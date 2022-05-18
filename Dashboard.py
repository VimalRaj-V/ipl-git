# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 11:53:30 2022

@author: Vimal Raj
"""

# import module

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("ipl_record_players.csv")
data_csv = data.copy()
data_csv["Team"] = data_csv["Team"].astype('category')
data_csv["Hs_vs"] = data_csv["Hs_vs"].astype(str)
teams =  list (set (data_csv["Team"].tolist()))

def run_splitup (player):
    sixes = int(player['sixes'])
    fours = int(player['fours'])
    score = int(player['batsmen_score'])
    runs_splitup = [["Sixes",sixes*6], ["fours", fours*4], ["Others", score - (sixes+fours)]]
    # Create the pandas DataFrame
    df = pd.DataFrame(runs_splitup, columns = ['name','runs'])
    return(df)

st.title("IPL Players Stats !!!")


# SideBar creation
st.sidebar.title("Select your team")
team = st.sidebar.selectbox("Select Team ", teams)
category = st.sidebar.radio("Select player category ", ('Batsman', 'Bowler', 'All rounder'))
team_players = data_csv[(data_csv.Team == team) & (data_csv.player_Category == category)]
team_players_name = list(team_players['Name'])
player = st.sidebar.selectbox("Select a player", team_players_name)
player_details = team_players[team_players.Name == player]


st.markdown(f"### {player}")
# MainBar creation


if category == 'Batsman':    
    # Left column - pie chart
    st.write(f"{player} has scored {int(player_details['batsmen_score'])} runs.")
    pie_col, gauge_col = st.columns((1,1))
    
    piedata = run_splitup(player_details)
    fig = px.pie(piedata, values='runs', names = 'name', hover_name='runs')
    fig.update_layout(showlegend = True, width=350, height=350,
    margin=dict(l=0.5,r=1,b=1,t=1))
    fig.update_traces(textposition='inside', textinfo='percent')
    pie_col.write(fig)
    
    # Right column - Gauge meter
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(player_details['strike_rate']),
        domain = {'x': [0.25, 0.75], 'y': [0.4, 0.8]},
        title = {'text': "Strike rate", 'font': {'size': 32}},
        gauge = {'axis': {'range': [None, 200]},
                 'bar': {'color': "darkblue"},
                     'steps' : [
                         {'range': [0, 100], 'color': "lavender"},
                         {'range': [100, 200], 'color': "cyan"}]})) 
    fig.add_trace(go.Indicator(
        mode = "number+gauge",
        gauge = {'shape': "bullet", 'bar': {'color': "darkblue"},
                 'axis': {'range': [None, 200]}},
        value = int(player_details["Innings"]),
        domain = {'x': [0.30, 0.85], 'y': [0.1, 0.3]},
        title = {'text': "Innings"},
        ))
    gauge_col.write(fig)
    opponent_team = set(player_details['Hs_vs'])
    st.success(f"Highest Score : {int(player_details['Highest_score'])}  vs  {opponent_team.pop()} (SR : {float(player_details['Hs_SR'])})")

elif category == 'Bowler':
    
    bar_col, gauge_col = st.columns((1,1))
    
    # Left column - Bar Chart
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Matches", "Wickets"],
        y=[int(player_details['matches']), int(player_details['Wickets'])],
        marker_color = ['orange', 'purple']))
    
    fig.update_layout( autosize = False, width=300, height=500)
    bar_col.write(fig)
    
    # Right column - Gauge meter
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(player_details['economy']),
        domain = {'x': [0, 0.5], 'y': [0, 1]},
        title = {'text': "Economy", 'font': {'size': 32}},
        gauge = {'axis': {'range': [None, 15]},
                 'bar': {'color': "cornflowerblue"},
                     'steps' : [
                         {'range': [0, 6], 'color': "darkseagreen"},
                         {'range': [6, 15], 'color': "indianred"}]})) 
    gauge_col.write(fig)
else:
    fig = go.Figure()
    
    # Left column - Gauge meter
    
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = float(player_details['strike_rate']),
        domain = {'x': [0, 0.4], 'y': [0, 1]},
        title = {'text': "Strike rate", 'font': {'size': 32}},
        gauge = {'axis': {'range': [None, 200]},
                 'bar': {'color': "darkblue"},
                     'steps' : [
                         {'range': [0, 100], 'color': "lavender"},
                         {'range': [100, 300], 'color': "cyan"}]})) 
    
    # Right column - Gauge meter
    
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = float(player_details['economy']),
        domain = {'x': [0.6, 1], 'y': [0, 1]},
        title = {'text': "Economy", 'font': {'size': 32}},
        gauge = {'axis': {'range': [None, 15]},
                 'bar': {'color': "cornflowerblue"},
                     'steps' : [
                         {'range': [0, 6], 'color': "darkseagreen"},
                         {'range': [6, 15], 'color': "indianred"}]})) 
    st.write(fig)
    opponent_team = set(player_details['Hs_vs'])
    st.success(f"Highest Score : {int(player_details['Highest_score'])}  vs  {opponent_team.pop()} (SR : {float(player_details['Hs_SR'])})")

