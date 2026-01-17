# What we need
from modules.get_wiki_tables_func import get_wiki_tables_func

# Arguments

# Page title, replace whitespaces with _
page_name = "List_of_largest_companies_in_the_United_States_by_revenue"
# Must send a header that looks like this: User-Agent: MyAppName/1.0 (myemail@example.com) 
your_app_name = "wikitable_extractor/1.0"
your_email = "thomas.duong@theinformationlab.co.uk"
# Specify which table to extract by its order, 1 = first table on the page, 2 = second table etc.
table_number = 1
# Enter the name of the output file without the .csv suffix
filename = "largest_companies"

get_wiki_tables_func(page_name, your_app_name, your_email, table_number, filename)