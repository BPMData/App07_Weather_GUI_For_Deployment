import streamlit as st
import requests
from datetime import datetime
from countries import better_country_converter, state_converter

weather_key = st.secrets["WEATHER_API"]

def format_dates(list):
    formatted_dates = []
    for date in list:
        dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        formatted_date = dt.strftime("%B %d - %I:%M %p")
        formatted_dates.append(formatted_date)
    return formatted_dates

def get_data_properly(lat,lon,days=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    nr_values_needed = 8*days
    filtered_data = filtered_data[:nr_values_needed]
    return filtered_data

def get_geo(city=None, state=None, country=None):
    country_code = None
    state_code = None
    if state is not "":
        state = state.title()
        print(state)
        state_code = state_converter[state]
        print(state_code)
    else:
        state_code = ""
    if country is not "":
        country = country.upper()
        print(country)
        country_code = better_country_converter[country]
        print(country_code)
    else:
        country_code = ""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state_code},{country_code}&limit=1&appid={weather_key}"
    response = requests.get(url)
    rawdata = response.json()
    needed = (rawdata[0]["lat"], rawdata[0]["lon"])
    return rawdata, needed