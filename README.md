# Elections-Scraper
#Voting Data Extraction Tool

A Python script for scraping voting results from the volby.cz website. The program downloads data from a specified URL, processes the election results for each municipality, and saves the results to a CSV file.
Features

    Scrapes voting data for individual municipalities.
    Aggregates and formats data in a structured CSV format.
    Handles navigation through multiple pages of results.

#Installation
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

Usage

    Run the Script:

    bash

python project_3.py

Arguments:

    URL: URL of the voting results page for the municipality.
    Output CSV file: Name of the CSV file to save the data.

Example:

bash

    python project_3.py "https://www.volby.cz/..." "results.csv"

The output will be saved in the specified CSV file.
Author

    Jakub Macíček
    Email: macicekjakub@gmail.com

For more details or assistance, feel free to reach out to the author.
