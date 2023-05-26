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
def run_devigger():
    # Get the input values
    leg_odds_decimal = leg_odds_input.value
    final_odd_decimal = final_odd_input.value

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

# Create text input widgets and button
leg_odds_input = st.text_input("Qouten", "1.9/1.9,1.9/1.9")
final_odd_input = st.text_input("Boost Q", "2.5")
button = st.button("Run Devigger API")

# Check if the button is clicked
if button:
    run_devigger()
