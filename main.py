# What we need
from modules.scrape_wiki_tables_func import scrape_wiki_tables

# Arguments
# Page title, replace whitespaces with _
page_name = "Wikipedia:Statistics"
# Must send a header that looks like this: User-Agent: MyAppName/1.0 (myemail@example.com) 
your_app_name = "scrape_wiki_tables/0.1"
your_email = "thomas.duong@theinformationlab.co.uk"
# Specify which table to extract: 1 = first table on the page, 2 = second table etc.
table_number = 7
# Enter the name of the output file without the .csv suffix
filename = "Wikipedia_Statistics"

# Function
scrape_wiki_tables(page_name, your_app_name, your_email, table_number, filename)