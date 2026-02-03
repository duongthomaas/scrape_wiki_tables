import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "parse",
    "page": "Guinness_World_Records",
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
table = soup.find_all('table', class_='wikitable')[1]

headers = table.find_all('th')

# Getting headers from the first table
headers_table = [title.text.strip() for title in headers]

# print(headers_table)

# Creating dataframe using pandas

df = pd.DataFrame(columns= headers_table)

# Finding data within the table

column_data = table.find_all('tr')
# print(column_data)

# Creating table, adding data under headers
# Dictionary to track cells that span down from previous rows
pending_cells = {}

for row_idx, row in enumerate(column_data[1:]):
    row_data = row.find_all('td')
    individual_row_data = []
    col_idx = 0
    
    for data in row_data:
        # First, add any pending cells from previous rowspans at this column position
        while col_idx in pending_cells.get(row_idx, {}):
            individual_row_data.append(pending_cells[row_idx][col_idx])
            col_idx += 1
        
        text = data.text.strip()
        colspan = int(data.get('colspan', 1))
        rowspan = int(data.get('rowspan', 1))
        
        # Add the cell data (duplicated for colspan)
        individual_row_data.extend([text] * colspan)
        
        # If rowspan > 1, store this cell for future rows
        if rowspan > 1:
            for future_row in range(1, rowspan):
                if row_idx + future_row not in pending_cells:
                    pending_cells[row_idx + future_row] = {}
                # Store the cell for each column it spans
                for col_offset in range(colspan):
                    pending_cells[row_idx + future_row][col_idx + col_offset] = text
        
        col_idx += colspan
    
    # Add any remaining pending cells at the end of the row
    while col_idx in pending_cells.get(row_idx, {}):
        individual_row_data.append(pending_cells[row_idx][col_idx])
        col_idx += 1
    
    length = len(df)
    df.loc[length] = individual_row_data


# Exporting output to .csv

# Create the folder 'output_table' if it doesn't exist yet
os.makedirs("output_table", exist_ok=True)

# Join the folder and filename safely
file_path = os.path.join("output_table", "guinness_records.csv")

# Now you can save your file
df.index = df.index + 1
df.to_csv(file_path, index=True) 
print(f"Saving to: {file_path}")