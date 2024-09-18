import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'NewYork Bikes Strategy Dashboard', layout='wide')
st.title("NewYork Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df_daily = pd.read_csv('necessary_data_to_plot.csv')
top20 = pd.read_csv('top20.csv', index_col = 0)


######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard will help address the distribution and expansion problems that New York's Citi Bike service is currently facing.")
    st.markdown("Currently, New York's bike-sharing service is experiencing issues with bike availability at certain stations and times. This analysis will look at the potential reasons behind this. The dashboard                  is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("NewYork_Bikes.jpg") 
    st.image(myImage)


    ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df_daily['date'], y = df_daily['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df_daily['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df_daily['date'], y = df_daily['avgTemp'], name = 'Daily temperature', marker={'color': df_daily['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022 NewYork',
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
  
    # Bar chart

   
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in Chicago',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that certain bike start stations are significantly more popular than others in New York. The top three stations are: W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 56 St.There is a big jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over NewYork")

    path_to_html = "NewYork_Bike_Trip_map.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in NewYork")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("W 21 St & 6 Ave, West St & Chambers St, Broadway & W 56 St.Based on the visualization, it seems that the most popular start stations do align with popular bike trips, particularly in central areas like around Central Park and downtown Manhattan. The stations W 21 St & 6 Ave and West St & Chambers St appear to be located in areas where there is high trip activity, as indicated on the map.")
    st.markdown("The most common bike routes are primarily centered in Manhattan, especially around major landmarks like Central Park, Columbia University, and NYU. There are also popular routes along the East River and Hudson River, connecting different parts of Manhattan and providing scenic rides.")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("NewYork Bikes.jpg")  
    st.image(bikes)
    st.markdown("### Our analysis has shown that NewYork's bike-sharing service should focus on the following objectives moving forward:")
    st.markdown("-The analysis shows that the most popular bike stations, particularly around W 21 St & 6 Ave and West St & Chambers St, coincide with high-density routes in central Manhattan, such as those near Central Park and NYU. There is a clear seasonal pattern where bike usage peaks during warmer months, with significantly fewer trips during the colder months.")
    st.markdown("-To optimize operations, increase bike availability at popular stations and reduce stock during colder months (November to April) by 25-40%. Additionally, consider adding more stations along high-demand waterfront routes and implementing real-time restocking strategies to ensure bikes are always available at key stations.")