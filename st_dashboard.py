######################################################### NEWYORK BIKES DASHBOARD #############################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


######################################################## Initial settings for the dashboard #####################################################


st.set_page_config(page_title = 'NewYork Bikes Strategy Dashboard', layout='wide')
st.title("NewYork Bikes Strategy Dashboard")
st.markdown("This dashboard will help address the distribution and expansion problems that New York's Citi Bike service is currently facing.")
st.markdown("Currently, New York's bike-sharing service is experiencing issues with bike availability at certain stations and times. This analysis aims to identify the root causes and propose actionable solutions to improve bike distribution and customer satisfaction.")

######################################################## Import Data #############################################################################

df_daily = pd.read_csv('necessary_data_to_plot.csv')
top20 = pd.read_csv('top20.csv', index_col = 0)

######################################################## Define the Charts ########################################################################

## Bar Chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in NewYork',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line Chart

fig = make_subplots(specs = [[{"secondary_y": True}]])

fig.add_trace(
go.Scatter(x = df_daily['date'], y = df_daily['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df_daily['bike_rides_daily'],'color': 'blue'}),
secondary_y = False
)

fig.add_trace(
go.Scatter(x=df_daily['date'], y = df_daily['avgTemp'], name = 'Daily temperature', marker={'color': df_daily['avgTemp'],'color': 'red'}),
secondary_y=True
)

fig.update_layout(
    title = 'Daily bike trips and temperatures in 2022 NewYork',
    height = 600
)

st.plotly_chart(fig, use_container_width=True)


### Add the map ###

path_to_html = "NewYork_Bike_Trip_map.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()
    
## Show in webpage
st.header("Bike Trips in NewYork")
st.components.v1.html(html_data,height=1000)
    