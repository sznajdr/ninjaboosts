
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
def run_devigger(leg_odds_decimal, final_odd_decimal):
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
    final_odd = convert_to_american(float(final_odd_decimal))

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

# Create a button to run the Devigger API
if st.button("Run Devigger API"):
    run_devigger(leg_odds_decimal, final_odd_decimal)

# Add pictures below the API stuff
st.header("anleitung:")
st.write("boost einzelwetten qouten suchen")
st.write("qouten wie im beispielformat eingeben: erste zahl immer das worauf man wettet, danach mit / getrennt die wetten dagegen, falls ein boost aus mehreren kombinierten wetten besteht das mit allen wetten wiederholen - getrennt durch komma!")
st.write("boost qoute eingeben")

st.image("https://github.com/sznajdr/ninjaboosts/blob/f153377f8098139843529e098978ea1713ae4d12/bway1.png&text=Image+1")
st.image("https://github.com/sznajdr/ninjaboosts/blob/f153377f8098139843529e098978ea1713ae4d12/antw1.png&text=Image+1")
st.image("https://github.com/sznajdr/ninjaboosts/blob/f153377f8098139843529e098978ea1713ae4d12/psv2.png&text=Image+1")

st.header("beispiel:")
st.write("1. ungefähr '1.9/1.9/1.9,1.9/1.9' im 'odds' feld.")
st.write("2. ca '2.5' im 'odds boost' feld.")
st.write("3. clickbutton")
st.write("4. EV% größer als null = value! vamos allez lesgo ")

st.image("https://github.com/sznajdr/ninjaboosts/blob/f153377f8098139843529e098978ea1713ae4d12/boost1.png&text=Image+1")


