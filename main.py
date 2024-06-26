import streamlit as st
import plotly.express as px
from countries import better_country_converter, state_converter, CC
from forecast_backend import format_dates, get_geo, get_data_properly


st.title("Generate a Custom Weather Forecast")
city = st.text_input("For which city would you like to know the weather?",
                     placeholder="Enter city name here", key="entered_city").casefold()

if city:
    capitalized_keys = [key.title() for key in better_country_converter.keys()]
    country = st.selectbox(options=capitalized_keys, label="Please select which country this city is in."
                                                           "  \n:violet[It's okay to leave this blank!]",
                           key="country_pick")
    state = st.selectbox(options=state_converter.keys(),label="If this city is in the U.S., please select which state it is in. "
                                                              ":pink[:violet[It's okay to leave this blank!]]",
                           key="state_pick")

days = st.slider("Number of Days to Forecast", min_value=1, max_value=5,
                 help="Select the number of days you'd like to know the weather forecast for.", key="days_pick")

forecast_type = st.selectbox(options=("Temperature", "Atmospheric Conditions"),
                             label=":green[Select type of data to view]", key="forecast_pick").casefold()

if city:
    try:
        arguments = (city, state, country)
        fullJSON, needed = get_geo(*arguments)
        weatherdata = get_data_properly(*needed, days)
        country_called_upon = fullJSON[0]["country"]
        country_called_upon = CC[country_called_upon].title()
        try:
            state_called_upon = fullJSON[0]["state"]
            comma = ", "
        except KeyError:
            state_called_upon = ""
            comma = ""
        if days == 1:
            st.subheader(f"{forecast_type.title()} for {city.title()} in {state_called_upon}{comma}{country_called_upon} tomorrow")
        else:
            st.subheader(f"{forecast_type.title()} for {city.title()} in {state_called_upon}{comma}{country_called_upon} for the next {days} days")
        stopflag = False
    #     except IndexError:
    #         fullJSON = ({"country": "NULL ISLAND", "state": "Down Under"}, 5)
    #         needed = (0, 0)
    #         weatherdata = get_data_properly(*needed, days)
    #         country_called_upon = fullJSON[0]["country"]
    #         country_called_upon = CC[country_called_upon].title()
    #         errorcity = "You selected a City/Country combination which does not exist :("
    #         try:
    #             state_called_upon = fullJSON[0]["state"]
    #             comma = ", "
    #         except KeyError:
    #             state_called_upon = ""
    #             comma = ""
    #         if days == 1:
    #             st.subheader(
    #                 f"{forecast_type.title()} for {errorcity} in {state_called_upon}{comma}{country_called_upon} tomorrow")
    #         else:
    #             st.subheader(
    #                 f"{forecast_type.title()} for {errorcity} in {state_called_upon}{comma}{country_called_upon} for the next {days} days")
    except KeyError:
        st.info("Oh no! You've selected a city and/or state and/or country combination which does not exist.")
        stopflag = True
    except IndexError:
        st.info("Oh no! You've selected a city and/or state and/or country combination which does not exist.")
        stopflag = True
else:
    st.subheader("")

if city and not stopflag:
    if forecast_type == "temperature":
        temperatures = [DAY["main"]["temp"] for DAY in weatherdata]
        dates = [DAY["dt_txt"] for DAY in weatherdata]
        figure = px.line(x=dates, y=temperatures, labels={"x": "Date",
                                              "y": "Temperatures (F)"})  # Notice labels accepts a DICTIONARY as its input.
        st.plotly_chart(figure)

    if forecast_type == "atmospheric conditions":
        images = {"Clear": "https://lh3.googleusercontent.com/d/1GslstA5FMGQdj9r2iiqp4yZ9Eoaoolab",
                  "Clouds": "https://lh3.googleusercontent.com/d/1O5PO5jYuIKUfVhNU1Oup_8lJWFPENGPe",
                  "Rain": "https://lh3.googleusercontent.com/d/1LHBE5RVm47jXY_rXGjWQPLWtuXjIhlpW",
                  "Snow": "https://lh3.googleusercontent.com/d/1cPFMhm_m3yRTHGsNxTuajfCEPJvowbre"}

        skies_description = [DAY["weather"][0]["description"].title() for DAY in weatherdata]
        skies_conditions = [DAY["weather"][0]["main"] for DAY in weatherdata]
        skies_description = [DAY["weather"][0]["description"].title() for DAY in weatherdata]
        dates = [DAY["dt_txt"] for DAY in weatherdata]
        new_dates = format_dates(dates)
        captions = [f"{date}, {desc}" for date, desc in zip(new_dates, skies_description)]
        image_paths = [images[condition] for condition in skies_conditions]
        st.image(image_paths, caption=captions, width=120)
