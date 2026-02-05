# scrape_wiki_tables

<img align="right" width="331" height="196" alt="scrape_wiki_tables logo" src="https://github.com/user-attachments/assets/33f509cf-2580-4907-affd-5ce7512e8ca4" />


A Python function to scrape data from Wikipedia tables and parse them into CSV files.

## Overview

`scrape_wiki_tables` automates the extraction of tabular data from Wikipedia pages, handling complex table structures including colspan and rowspan attributes, and exports the results to clean CSV files. This tool is particularly useful for data analysis projects that require Wikipedia data in a structured format.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [Requirements](#requirements)
- [Features](#features)
- [How It Works](#how-it-works)
- [Caveats](#caveats)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/scrape_wiki_tables.git
cd scrape_wiki_tables
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install beautifulsoup4 pandas requests unidecode
```

## Usage

The main file to use is `main.py`.

### Basic Example

```python
from modules.scrape_wiki_tables_func import scrape_wiki_tables

# Arguments
# Page title - replace whitespaces with underscores
page_name = "List_of_public_corporations_by_market_capitalization"

# User-Agent header (required by Wikipedia)
# Must follow format: User-Agent: AppName/Version (email@example.com)
your_app_name = "scrape_wiki_tables/0.1"
your_email = "thomas.duong@theinformationlab.co.uk"

# Specify which table to extract: 1 = first table, 2 = second table, etc.
table_number = 1

# Output filename (without .csv extension)
filename = "List_of_public_corporations_by_market_capitalization"

# Run the function
scrape_wiki_tables(page_name, your_app_name, your_email, table_number, filename)
```

### Function Parameters

| Parameter       | Type  | Description                                       | Example                      |
| --------------- | ----- | ------------------------------------------------- | ---------------------------- |
| `page_name`     | `str` | Wikipedia page title (use underscores for spaces) | `"List_of_countries_by_GDP"` |
| `your_app_name` | `str` | Your application name and version                 | `"MyApp/1.0"`                |
| `your_email`    | `str` | Your contact email (required by Wikipedia)        | `"user@example.com"`         |
| `table_number`  | `int` | Which table to extract (1-indexed)                | `1` (first table)            |
| `filename`      | `str` | Output CSV filename (without extension)           | `"gdp_data"`                 |

### Finding the Right Page Name

The page name is the part of the Wikipedia URL after `https://en.wikipedia.org/wiki/`. For example:

- URL: `https://en.wikipedia.org/wiki/List_of_countries_by_GDP`
- Page name: `List_of_countries_by_GDP`

## Output

CSV files are saved to the `output_table/` folder in the same repository. The folder is created automatically if it doesn't exist.

Output file path: `output_table/<filename>.csv`

### Output Format

- **Encoding**: UTF-8
- **Separator**: Comma (`,`)
- **Headers**: First row contains column names
- **Index**: Not included in output
- **Special characters**: Diacritics removed (e.g., é → e, ñ → n)

## Requirements

```txt
beautifulsoup4>=4.9.0
pandas>=1.0.0
requests>=2.25.0
unidecode>=1.2.0
```

**Python Version**: 3.6+

Install dependencies with:

```bash
pip install beautifulsoup4 pandas requests unidecode
```

## Features

- ✅ **Handles complex table structures**: Correctly processes tables with `colspan` and `rowspan` attributes
- ✅ **Text normalization**: Removes diacritics and accents from text (e.g., é → e, ñ → n)
- ✅ **Automatic header cleaning**: Removes empty header values
- ✅ **Smart directory management**: Automatically creates output directory if it doesn't exist
- ✅ **Fallback mechanism**: Uses placeholder headers when extraction fails
- ✅ **Wikipedia compliant**: Includes proper User-Agent headers as required by Wikipedia's API guidelines
- ✅ **Multiple table support**: Can extract any specific table from a page with multiple tables
- ✅ **Robust parsing**: Handles both `<thead>` and header rows without explicit `<thead>` tags

## How It Works

1. **Page Retrieval**: Sends an HTTP request to Wikipedia with a proper User-Agent header
2. **HTML Parsing**: Uses BeautifulSoup to parse the HTML content
3. **Table Selection**: Identifies and selects the specified table (based on `table_number`)
4. **Header Extraction**: Extracts column headers from the first row
5. **Data Processing**:
   - Iterates through each table row
   - Handles `colspan` (cells spanning multiple columns)
   - Handles `rowspan` (cells spanning multiple rows)
   - Tracks pending cells from previous rows
6. **Text Cleaning**: Removes diacritics and whitespace
7. **DataFrame Creation**: Builds a pandas DataFrame with the extracted data
8. **CSV Export**: Saves the DataFrame to a CSV file

### Handling colspan and rowspan

The function intelligently handles complex table structures:

**colspan example:**

```html
<td colspan="3">Value</td>
```

This becomes three columns with the same value: `['Value', 'Value', 'Value']`

**rowspan example:**

```html
<td rowspan="2">Value</td>
```

This value appears in the same column position for two consecutive rows.

## Caveats

- **Multi-row headers**: The programme extracts only the first row of headers. If a Wikipedia table has headers spanning multiple rows (e.g., grouped column headers), only the first row will be captured.
- **Header fallback**: If header extraction fails or the number of headers doesn't match the number of columns, placeholder headers (0, 1, 2, 3, ...) are used instead. This typically happens when:
  - The table structure is malformed
  - Headers use unusual HTML elements
  - Column counts don't match between headers and data rows

- **Wikipedia compliance**: Always provide a valid User-Agent header with your contact information as required by [Wikipedia's API guidelines](https://www.mediawiki.org/wiki/API:Etiquette). Failure to do so may result in your requests being blocked.

- **Table identification**: Tables are identified by the `wikitable` CSS class. Some Wikipedia tables may use different classes and won't be detected.

- **English Wikipedia only**: Currently configured for English Wikipedia (`en.wikipedia.org`). Other language versions require URL modification.

## Best Practices

1. **User-Agent**: Always use a descriptive app name and valid email address
2. **Rate limiting**: Avoid making rapid consecutive requests to Wikipedia
3. **Data validation**: Always verify the output CSV matches your expectations
4. **Page selection**: Check the Wikipedia page in a browser first to identify which table you need
5. **Error handling**: Wrap function calls in try-except blocks for production use

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Open a Pull Request

### Areas for Improvement

- Support for multi-row header concatenation
- Support for non-English Wikipedia versions
- Better handling of nested tables
- Progress indicators for large tables
- Batch processing multiple pages
- Custom column name mapping
- Data type inference and conversion

## Future Enhancements

- [ ] Add support for concatenating multi-row headers
- [ ] Support for other Wikipedia language versions
- [ ] Command-line interface (CLI)
- [ ] Logging functionality
- [ ] Unit tests
- [ ] Table preview before extraction
- [ ] Custom CSS class selectors for table identification

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

**Thomas QL Duong**  
Email: [thomas.duong@theinformationlab.co.uk](mailto:thomas.duong@theinformationlab.co.uk)  
Organization: The Information Lab

---

**Note**: This tool is for educational and research purposes. Please respect Wikipedia's [Terms of Use](https://foundation.wikimedia.org/wiki/Terms_of_Use) and avoid excessive automated requests.
