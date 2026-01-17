import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "parse",
    "page": "List_of_countries_by_alcohol_consumption_per_capita",
    "format": "json",  
    "prop": "text"
}

headers = {
    "User-Agent": "wikitable_extractor/1.0 (thomas.duong@theinformationlab.co.uk)"
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
table = soup.find_all('table', class_='wikitable')[2]
# print(table)

headers = table.find_all('th')

# # Getting headers from the first table
headers_table = [title.text.strip() for title in headers]

# # Creating dataframe using pandas

df = pd.DataFrame(columns= headers_table)

# # Finding data within the table

column_data = table.find_all('tr')

# # Creating table, adding data under headers
for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    
    length = len(df)
    df.loc[length] = individual_row_data

# Exporting output to .csv
# df.to_csv(r'C:\Users\ThomasDuong\Documents\GitHub\webpage_table_extractor\output_table\companies.csv', index = False)

print(df)