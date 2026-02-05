import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from unidecode import unidecode

url = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "parse",
    "page": "Wikipedia:Statistics",
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
table = soup.find_all('table', class_= ['wikitable', 'ratingstable'])[6]

# Try to extract headers
headers = table.find_all('tr')[0] # Taking only the first row in headers ---- This will ignore any subsequent rows possibly containing headers

headers_table = [title.text.strip() for title in headers]

# Removing empty values within a list
headers_table_cleaned = []
for i in headers_table:
    if i != '':
        headers_table_cleaned.append(i)

# Creating dataframe using pandas
df = pd.DataFrame(columns=headers_table_cleaned)
# print(df)
    
# Finding data within the table
column_data = table.find_all('tr')
if column_data[1].find_all('td'): # If there's <td> values in the second row, loops will start at index 1
    starting_row = column_data[1:]
else:
    starting_row = column_data[2:] # Else -> start at index 2 because index 1 contains headers

# Creating table, adding data under headers
# Dictionary to track cells that span down from previous rows
pending_cells = {} # Creates an empty dictionary. Structure will be: {row_index: {column_index: text}} to remember which cells from previous rows need to appear in future rows.
all_rows_data = []  # Store all row data first before adding to dataframe

for row_idx, row in enumerate(starting_row): # Loops through each row (skipping the header at index 0 or 1). enumerate gives us both the index (row_idx) and the actual row element.
    row_data = row.find_all(['td', 'th']) # Finds all the <td> and <th> (table cell) elements in this row.
    individual_row_data = [] # Creates an empty list to store the final data for this row (including duplicated cells from colspan/rowspan).
    col_idx = 0 # Tracks which column position we're currently at (0 = first column, 1 = second column, etc.).
    
    for data in row_data: # Loops through each actual <td> cell in the current row.
        # First, add any pending cells from previous rowspans at this column position
        while col_idx in pending_cells.get(row_idx, {}): # Before processing the current cell, check if there are any cells from previous rows (with rowspan) that should appear at the current column position. pending_cells.get(row_idx, {}) returns the dictionary of pending cells for this row, or an empty dict if there are none.
            individual_row_data.append(pending_cells[row_idx][col_idx]) # Add the pending cell's text to our row data.
            col_idx += 1 # Move to the next column since we just filled this one with a pending cell.
        
        text = data.text.strip() # Extract the text content from the current <td> and remove leading/trailing whitespace.
        colspan = int(data.get('colspan', 1)) # Get the colspan attribute value. If it doesn't exist, default to 1 (cell spans 1 column).
        rowspan = int(data.get('rowspan', 1)) # Get the rowspan attribute value. If it doesn't exist, default to 1 (cell spans 1 row only).
        
        # Add the cell data (duplicated for colspan)
        individual_row_data.extend([text] * colspan) # Add the cell's text to our row data. If colspan=3, this adds the text 3 times: [text, text, text].
        
        # If rowspan > 1, store this cell for future rows
        if rowspan > 1: # Check if this cell spans multiple rows downward.
            for future_row in range(1, rowspan): # Loop through each future row this cell affects. range(1, rowspan) means if rowspan=3, we loop for rows 1 and 2 ahead (not row 0, which is the current row).
                if row_idx + future_row not in pending_cells:
                    pending_cells[row_idx + future_row] = {} # If we haven't created an entry for this future row yet in pending_cells, create an empty dictionary for it.
                # Store the cell for each column it spans
                for col_offset in range(colspan): # Loop through each column this cell occupies (important if the cell has both colspan and rowspan).
                    pending_cells[row_idx + future_row][col_idx + col_offset] = text # Store the cell's text at the specific future row and column position. For example, if current position is column 2 and colspan=2, we store at columns 2 and 3.
        
        col_idx += colspan # Move our column tracker forward by the number of columns this cell occupied.
    
    # Add any remaining pending cells at the end of the row
    while col_idx in pending_cells.get(row_idx, {}): # After processing all actual <td> cells, check if there are any more pending cells (from previous rowspans) that should appear at the end of this row.
        individual_row_data.append(pending_cells[row_idx][col_idx])
        col_idx += 1 # Add those remaining pending cells and increment the column position.

    # Removing all the accents (diacritics) in characters.
    individual_row_data_unidecode = []
    for i in individual_row_data:
        individual_row_data_unidecode.append(unidecode(i))
    
    # Store this row's data to be added later
    all_rows_data.append(individual_row_data_unidecode)

# Now add all rows to the appropriate dataframe
try:
    # Add the completed row data to the dataframe at the next available index position.
    for row_data in all_rows_data:
        length = len(df)
        df.loc[length] = row_data
except ValueError:
    try:
        # Alternative when parsing headers fails - create placeholders for headers and add existing rows to those placeholders
        # Create placeholder column names based on the number of columns in the first row
        num_columns = len(all_rows_data[0])
        placeholder_columns = []
        for i in range(num_columns):
            placeholder_columns.append(i)
        df = pd.DataFrame(all_rows_data, columns=placeholder_columns)
    except ValueError:
        # Another alternative when the first alternative fails - create placeholders for headers and add existing rows to those placeholders
        # Create placeholder column names based on the number of columns in the second row
        num_columns = len(all_rows_data[1])
        placeholder_columns = []
        for i in range(num_columns):
            placeholder_columns.append(i)
        df = pd.DataFrame(all_rows_data, columns=placeholder_columns)

# Exporting output to .csv
# Create the folder 'output_table' if it doesn't exist yet
os.makedirs("output_table", exist_ok=True)

# Join the folder and filename safely
file_path = os.path.join("output_table", "Wikipedia_Statistics2.csv")

# Now you can save your file
# df.index = df.index + 1

df.to_csv(file_path, index=False, mode='w') 
print(f"Saving to: {file_path}")