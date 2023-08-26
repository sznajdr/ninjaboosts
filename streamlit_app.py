
import requests
import streamlit as st

# Function to convert decimal odds to American odds
def convert_to_american(decimal_odds):
    if decimal_odds >= 2:
        american_odds = round((decimal_odds - 1) * 100)
        return str(american_odds)
    else:
        american_odds = round(-100 / (decimal_odds - 1))
        return str(american_odds)

# Define the function to handle button click
def run_devigger(leg_odds_decimal, final_odd_decimal, check_box):
    # Split the leg odds into individual sets
    leg_odds_sets = leg_odds_decimal.split(",")

    # Convert decimal odds to American odds for each set
    converted_leg_odds = []
    for odds_set in leg_odds_sets:
        odds = odds_set.split("/")
        converted_odds = "/".join(convert_to_american(float(odd)) for odd in odds)
        converted_leg_odds.append(converted_odds)

    # Join the converted odds sets
    leg_odds = ",".join(converted_leg_odds)
    final_odd = float(final_odd_decimal)
    if check_box:
        final_odd *= 0.947
    final_odd = convert_to_american(final_odd)

    # Define the API URL
    url = "https://api.crazyninjaodds.com/api/devigger/v1/sportsbook_devigger.aspx?api=open"

    # Set the parameters for the request
    parameters = {
        "LegOdds": leg_odds,
        "FinalOdds": final_odd,
        "DevigMethod": 0,
        "Args": "ev_p"
    }

    # Send the GET request
    response = requests.get(url, params=parameters)

    # Check the response status
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Extract the EV_Percentage
        ev_percentage = data["Final"]["EV_Percentage"]

        # Print the expected value percentage
        st.write("Expected Value: {}%".format(ev_percentage * 100))
    else:
        st.write("Request failed with status code:", response.status_code)

# Create text input widgets
leg_odds_decimal = st.text_input("odds", "1.9/1.9,1.9/1.9")
final_odd_decimal = st.text_input("odds boost", "2.5")
check_box = st.checkbox("steuer")

# Create a button to run the Devigger API
if st.button("Run Devigger API"):
    run_devigger(leg_odds_decimal, final_odd_decimal, check_box)

# Add pictures below the API stuff
st.header("anleitung:")
st.write("boost einzelwetten qouten suchen")
st.write("qouten wie im beispielformat eingeben: erste zahl immer das worauf man wettet, danach mit / getrennt die wetten dagegen, falls ein boost aus mehreren kombinierten wetten besteht das mit allen wetten wiederholen - getrennt durch komma!")
st.write("boost qoute eingeben")

st.markdown("[![Image](https://github.com/sznajdr/ninjaboosts/blob/main/bway1.png?raw=true&text=Image+1)](https://github.com/sznajdr/ninjaboosts/blob/main/bway1.png?raw=true&text=Image+1)")


st.header("beispiel:")

st.write("qouten auf oddsportal.de raus suchen, aufs spiel klicken und PINNACLE qouten benutzen")


st.markdown("[![Image](https://github.com/sznajdr/ninjaboosts/blob/main/antw1.png?raw=true&text=Image+1)](https://github.com/sznajdr/ninjaboosts/blob/main/antw1.png?raw=true&text=Image+1)")
st.markdown("[![Image](https://github.com/sznajdr/ninjaboosts/blob/main/psv2.png?raw=true&text=Image+1)](https://github.com/sznajdr/ninjaboosts/blob/main/psv2.png?raw=true&text=Image+1)")


st.write("1. ungefähr ' 1.9/1.9/1.9,1.9/1.9 ' im odds feld.")
st.write("2. ca ' 2.5 ' oder so - boost qoute! - im odds boost feld.")
st.write("3. clickbutton")
st.write("4. EV% größer als null = value! vamos allez lesgo ")

st.markdown("[![Image](https://github.com/sznajdr/ninjaboosts/blob/main/boost1.png?raw=true&text=Image+1)](https://github.com/sznajdr/ninjaboosts/blob/main/boost1.png?raw=true&text=Image+1)") 

# Add list of bookmakers
st.header("buchmacher:")
st.write("https://bet365.de (Steuer)")
st.write("https://bildbet.de (Steuer)")
st.write("https://betano.de -> scrollen bis 'Verbesserte Qouten', ab und zu an großkampftagen auch 'Super verbesserte Qouten' die müssten fast immer gut sein (Steuer)")
st.write("https://sports.betway.de/en/sports/cat/betway-boosts -> oft zweidrei gute, rest mal so mal so (Steuer)")
st.write("https://www.winamax.de/sportwetten/sports/10000")
st.write("https://neobet.de -> in den Spielen oben and und zu vorgeschlagene boosts (Steuer))") 



st.markdown("[![Image](https://github.com/sznajdr/ninjaboosts/blob/main/whitelist.png?raw=true&text=Image+1)](https://github.com/sznajdr/ninjaboosts/blob/main/whitelist.png?raw=true&text=Image+1)")


 

