 Elections-Scraper
# Voting Data Extraction Tool

A Python script for scraping voting results from the volby.cz website. The program downloads data from a specified URL, processes the election results for each municipality, and saves the results to a CSV file.
Features

- Scrapes voting data for individual municipalities
- Aggregates and formats data in a structured CSV format
- Handles navigation through multiple pages of results.

# Installation
Prerequisites

    Python 3.6+: Ensure Python is installed on your system. You can download it from python.org.

Dependencies

The script requires the following Python libraries:

    requests: For downloading web page content.
    BeautifulSoup4: For parsing HTML data.
    pandas: For data manipulation and saving to CSV.

Installation of Libraries

Install the required libraries using pip:

bash

pip install requests beautifulsoup4 pandas

# Usage

1. Run the Scrip

    python project_3.py

2. Arguments

    URL: URL of the voting results page for the municipality.

   
    Output CSV file: Name of the CSV file to save the data.

The output will be saved in the specified CSV file.
# Example:

    python project_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7101" "results.csv"


results.csv: 

    Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Kód obce,Občanská demokratická strana,Řád národa - Vlastenecká unie...
    523917,Bělá pod Pradědem,945,1546,938,77,1,0,47,2,53,70,8,12,10,0,1,79,1,33...
    524891,Bernartice,344,703,343,24,0,0,25,1,6,38,1,1,1,0,0,15,0,5,149,2,1,13...
    525227,Bílá Voda,140,242,138,17,1,0,7,1,5,14,6,2,0,0,0,13,0,9,18,1,0,16,0,0,...



# Author

- Jakub Macíček
- Email: macicekjakub@gmail.com

For more details or assistance, feel free to reach out to the author.
