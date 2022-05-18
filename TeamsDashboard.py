# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:09:12 2022

@author: Vimal Raj
"""


# import module

import pandas as pd
import streamlit as st

data = pd.read_csv("Teams_processed.csv")
data_csv = data.copy()

data_csv["team_name"] = data_csv["team_name"].astype('category')

# converting to list
teams =  data_csv["team_name"].tolist()
# Title
st.title("IPL Teams !!!")

# first argument takes the titleof the selectionbox
# second argument takes options
team = st.selectbox("Select Team ", teams)

runs = data_csv.at[teams.index(team), "total_runs"]

st.write(f"{team} has scored {runs} runs")