import streamlit as st
import datetime
import requests
import pandas as pd

st.set_page_config(
            page_title="Quick reference", # => Quick reference - Streamlit
            page_icon="🐍",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed

"""
## Welcome to Taxi Fare predictions
"""
columns_0 = st.columns(2)

user_date = columns_0[0].date_input(
    "When do you want to travel?",
    datetime.date(2023, 12, 1))

user_time = columns_0[1].time_input("Time:",
                     datetime.time(8,45,0))

pu_datetime = datetime.datetime.combine(user_date, user_time)

columns = st.columns(4)

pu_long = columns[0].number_input("Pick-up longitude:", min_value=-74.3, max_value=-73.7, value=-74.2)

pu_lat = columns[1].number_input('Pick-up latitude:', min_value=40.5, max_value=40.9, value=40.6)

do_long = columns[2].number_input("Drop-off longitude:", min_value=-74.3, max_value=-73.7, value=-74.2)

do_lat = columns[3].number_input('Drop-off latitude:', min_value=40.5, max_value=40.9, value=40.8)

"""
*Be careful, longitudes must be between -74.3 and -73.7.
Latitudes must be between 40.5 and 40.9.*
"""

df_map = pd.DataFrame(
    {
        "latitude": [pu_lat, do_lat],
        "longitude": [pu_long, do_long]
    }
)
st.map(df_map, zoom=11)

passengers = int(st.number_input('How many passengers will be there?', min_value=1))

params = {
"pickup_datetime" : pu_datetime,
"pickup_longitude": pu_long,
"pickup_latitude": pu_lat,
"dropoff_longitude": do_long,
"dropoff_latitude": do_lat,
"passenger_count": passengers
}
url = 'https://taxifare.lewagon.ai/predict'

if st.button('Calculate'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    response = round(requests.get(url, params=params).json()["fare"], 2)
    st.write('Estimated fares are:')
    st.write(f"{response} $US")
