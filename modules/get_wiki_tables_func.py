# What we need
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Building function
def get_wiki_tables_func(page_name, your_app_name, your_email, table_number, filename):

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "parse",
        "page": page_name,
        "format": "json",  
        "prop": "text"
    }

    headers = {
        "User-Agent": f"{your_app_name} ({your_email})"
    }

    response = requests.get(url, params=params, headers=headers)

    # 1. Convert the API response to a Python Dictionary (JSON)
    data = response.json()

    # 2. Extract the actual HTML string from the JSON structure
    # Structure is: data -> 'parse' -> 'text' -> '*' (This asterisk holds the HTML)
    raw_html = data['parse']['text']['*']

    # 3. NOW feed the clean HTML to BeautifulSoup
    soup = BeautifulSoup(raw_html, 'html.parser')

    # 4. Find your table
    # Note: Wikipedia class names often change or have extra spaces. 
    # It is safer to select just "wikitable" or "sortable".
    table_number -= 1

    table = soup.find_all('table', class_='wikitable')[table_number]

    headers = table.find_all('th')

    # Getting headers from the first table
    headers_table = [title.text.strip() for title in headers]

    # Creating dataframe using pandas

    df = pd.DataFrame(columns= headers_table)

    # Finding data within the table

    column_data = table.find_all('tr')

    # Creating table, adding data under headers
    for row in column_data[1:]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]
        
        length = len(df)
        df.loc[length] = individual_row_data

    # Exporting output to .csv

    # Create the folder 'output_table' if it doesn't exist yet
    os.makedirs("output_table", exist_ok=True)

    # Join the folder and filename safely
    file_path = os.path.join("output_table", f"{filename}.csv")

    # Now you can save your file
    df.to_csv(file_path, index=False)  
    print(f"Saving to: {file_path}")