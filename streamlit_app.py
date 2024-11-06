import csv
import re
import time
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
import unicodedata

def get_data():
    url = 'https://www.winamax.de/sportwetten/sports/100000'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Use prettify() method to format HTML output
    pretty_html = soup.prettify()

    # Write output to a text file
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(pretty_html)

    # Read in the file
    with open('output.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    text = unicodedata.normalize('NFKD', text)
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
    text = text.replace('\u00e4', 'ae').replace('\u00f6', 'oe').replace('\u00fc', 'ue').replace('\u00a0', ' ')


    # Write the modified text back to the file
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(text)        
        
    # Open the file and read its contents
    with open('output.txt', 'r') as f:
        data = f.read()

    data = unicodedata.normalize('NFKD', data)    

    data = data.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
    data = data.replace('\u00e4', 'ae').replace('\u00f6', 'oe').replace('\u00fc', 'ue').replace('\u00a0', ' ')

    # Find all occurrences of the pattern to extract ID-label pairs
    pattern_boosts = r'"(\d+)":{"label":"([^"]+)","available":true,"code":"yes"}'
    matches_boosts = re.findall(pattern_boosts, data)

    # Create a dictionary to store the ID-label pairs
    id_boost_dict = {}
    for match in matches_boosts:
        id_boost_dict[match[0]] = {'boost': match[1], 'prevOdd': None, 'odds': None}

    # Extract the odds data and store it in a dictionary
    odds_data = data.split('"odds":{')[1].split('},"cc"')[0]
    odds_dict = eval('{' + odds_data + '}')
    for id, odds in odds_dict.items():
        if id in id_boost_dict:
            id_boost_dict[id]['odds'] = odds

    # Find all occurrences of the pattern to extract previous odds
    pattern_prev_odds = r'"previousOdd":([\d.]+)'
    matches_prev_odds = re.findall(pattern_prev_odds, data)
    for i, match in enumerate(matches_prev_odds):
        id_boost_dict[list(id_boost_dict.keys())[i]]['prevOdd'] = match

    return id_boost_dict


def save_to_csv(id_boost_dict):
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['boost', 'prevOdd', 'odds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for id, data in id_boost_dict.items():
            boost = data['boost'].replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
            prevOdd = str(data['prevOdd']).replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
            odds = str(data['odds']).replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
            writer.writerow({'boost': boost, 'prevOdd': prevOdd, 'odds': odds})



def main():
    st.set_page_config(page_title='-', page_icon='🎲')

    while True:
        try:
            id_boost_dict = get_data()
            save_to_csv(id_boost_dict)
            df = pd.read_csv('output.csv', usecols=['boost', 'prevOdd', 'odds'])
            st.table(df)
        except IndexError:
            data = {'boost': [':('], 'prevOdd': [':('], 'odds': [':(']}
            df = pd.DataFrame(data)
            st.table(df)
            time.sleep(60 * 60 * 3) # Wait for 3 hours
        else:
            time.sleep(60 * 60 * 3) # Wait for 3 hours
        
if __name__ == '__main__':
    main()
