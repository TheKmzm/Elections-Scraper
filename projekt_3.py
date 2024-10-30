"""
projekt_3.py: third project for the Engeto Online Python Academy

author: Jakub Macíček

email: macicekjakub@gmail.com

discord: TheKmzm
"""

import requests  # Library for downloading website content
from bs4 import BeautifulSoup  # Library for parsing HTML code
import pandas as pd  # Library for working with data and saving to CSV
import sys  # Library for exiting the program on error

# Function for parsing command-line arguments
def parse_arguments():
    """
    This function processes the arguments passed to the script from the command line.
    It expects two arguments:
    1. The URL of the area from which the data will be downloaded.
    2. The name of the output CSV file where the results will be saved.
    
    If the arguments are not provided correctly, the program exits with an error message.
    """
    
    try:
        args = [str(sys.argv[1]), str(sys.argv[2])]
        arg1 = args[0]
        arg2 = args[1]
        # Verify that the URL starts with the correct link
        if not("https://www.volby.cz" == arg1[:20]):
            print("Error: Enter a valid link to the volby.cz website")
            sys.exit(1)  # Exit the program if the URL is incorrect
        if not(".csv" == arg2[-4:]):
            print("Error: Enter a valid CSV file.")  
            sys.exit(1)  # Exit the program if the file name is not a CSV
        
    except:
        # If arguments are missing or invalid, print an error and exit
        print("Incorrect arguments!")
        sys.exit(0)

    return args  # Return the parsed arguments

# Function for downloading the HTML content of a page
def download_page(url):
    """
    This function takes a URL, downloads the page content using requests,
    and returns the structured HTML content using BeautifulSoup.
    If there's an error downloading the page, the program exits.
    """
    response = requests.get(url)  # Fetch the page content

    # Check if the page was downloaded successfully
    if response.status_code != 200:
        print(f"Error loading page: {url}")
        sys.exit(1)  # Exit the program if the page cannot be loaded

    # Return the loaded and parsed HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Function for extracting data from the results table
def extract_results(url):
    """
    This function takes the HTML content of a page, finds the table with election results,
    and extracts data on individual municipalities and voting results.
    Returns a list of data where each element contains information about one municipality.
    """
    # Download the HTML page using the provided URL
    soup = download_page(url)
    data_to_file = []  # List to store extracted data
    
    # Find the first table on the page (assuming it contains election results)
    tables = soup.find_all('table')
    is_header = False  # Flag to ensure the header row is only created once
    if not tables:
        print("Error: Results table not found.")
        sys.exit(1)  # Exit the program if the table does not exist

    # Process each table on the page (assuming the first few tables have needed data)
    for i in range(3):
        
        table = tables[i]
        rows = table.find_all('tr')  # Get all rows in the table
        
        counter = 0  # To skip the first two rows if they are headers
        # Extract data for each table row
        for row in rows:
            data = []  # List to store data for the current row
            if counter < 2:
                counter += 1
                continue  # Skip header rows
            
            # Get all columns from the row
            columns = row.find_all('td')
            code, name = extract_obec(columns)  # Get municipality code and name
            if name == "-":
                break  # Stop if invalid name is encountered
            data.append(code), data.append(name)  # Add municipality info to data list
            link_to_second = columns[2].find('a')['href']  # Link to detailed results
            second_page = download_page("https://www.volby.cz/pls/ps2017nss/" + link_to_second)
            votes = [0] * 28  # Initialize vote counts for parties
            # Check if there’s another page with further details
            if not(is_final_page(second_page)):
                tables_links = second_page.find('table').find_all('tr')[1:]
                table_links = tables_links[0].find_all('a')  # Links to each district
                
                for link2 in table_links:
                    link3 = link2['href']  # Link to third-level page
                    third_page = download_page("https://www.volby.cz/pls/ps2017nss/" + link3)
                    # Sum votes from the third-level page
                    votes = list(map(lambda a, b: a + b, votes, extract_votes(third_page, "third")))
                for v in votes:
                    data.append(v)  # Append each party's vote count
                
            else:
                # If there’s no third-level page, extract votes from the second page
                votes = extract_votes(second_page, "second")
                for v in votes:
                    data.append(v)
                
            data_to_file.append(data)  # Add all municipality data to final list
        # Create the header only once
        if not(is_header):
            header = headerf(third_page)
            is_header = True
            data_to_file.insert(0, header)  # Insert header at the top of data list
    return data_to_file  # Return the list of all extracted data

# Function to check if a page is the final page in the data sequence
def is_final_page(page):
    identificator = page.find('table').find('tr').find('th').text.strip()
    if identificator == "Okrsek":
        return False  # Not the final page if it contains district info
    return True

# Function to extract municipality code and name
def extract_obec(columns):
    obec_code = columns[0].text.strip()  # Municipality code
    obec_name = columns[1].text.strip()  # Municipality name
    return (obec_code, obec_name)

# Function to process the final level of detail in results
def final_page(second_page):
    tables_links = second_page.find('table').find_all('tr')[1:]
    table_links = tables_links[0].find_all('a')
    for link2 in table_links:
        link3 = link2['href']
        third_page = download_page("https://www.volby.cz/pls/ps2017nss/" + link3)
        extract_votes(third_page, "third")

# Function to create the header for the output file
def headerf(page):
    table = page.find_all('table')
    parties = []  # List to store party names
    header_start = ["Municipality Code", "Municipality Name", "Voters Listed", "Envelopes Issued", "Valid Votes"]
    for i in range(2):
        i += 1
        for party in table[i].find_all('tr')[2:]:
            columns_parties = party.find_all('td')
            party_name = columns_parties[1].text.strip()
            parties.append(party_name)  # Add each party name to the list
    parties.pop()  # Remove the last entry if needed
    # Add main header elements to the beginning of the list
    for i in range(5):
        i = -i
        parties.insert(0, header_start[i])
    return parties  # Return the header list

# Function to extract vote counts from the page
def extract_votes(page, number):
    a = 0
    b = 2
    data = []  # List to store vote counts and summary data
    if number == "third":
        a = -3
        b = 1
    table = page.find_all('table')
    columns = (table[0].find_all('tr')[b:])[0].find_all('td')
    voters = columns[3 + a].text.strip().replace('\xa0', '')  # Total voters
    envelopes_issued = columns[4 + a].text.strip().replace('\xa0', '')  # Envelopes issued
    valid_votes = columns[7 + a].text.strip().replace('\xa0', '')  # Valid votes
    data.append(int(envelopes_issued)), data.append(int(voters)), data.append(int(valid_votes))
    
    # Process party vote counts
    for i in range(2):
        i = i + 1
        for party in table[i].find_all('tr')[2:]:
            columns_parties = party.find_all('td')
            data.append(int(columns_parties[2].text.strip().replace("-", "0")))
    data.pop()  # Remove the last entry if not needed
    return data  # Return list of vote data

# Function for saving data to CSV
def save_to_csv(data, output_file):
    """
    This function accepts extracted data (a list of municipalities and their election results),
    the name of the output file, and the header (column names) and saves the data to a CSV file
    using the pandas library.
    """
    header = data[0]
    data.pop(0)  # Remove the header row from data
    df = pd.DataFrame(data, columns=header)  # Create a DataFrame with the data and header
    df.to_csv(output_file, index=False)  # Save the DataFrame to a CSV file
    print(f"Results successfully saved to {output_file}")  # Print confirmation of successful save

# Main program function
def main():
    """
    The main program function that controls the entire process:
    1. Loads command-line arguments.
    2. Downloads page content according to the provided URL.
    3. Extracts data from the election results table.
    4. Saves the results to a CSV file according to the specified filename.
    """
    args = parse_arguments()  # Load arguments (URL and output file)
    
    # Extract election results data from the loaded page
    data = extract_results(args[0])
    
    # Save the results to a CSV file
    save_to_csv(data, args[1])

# Run the main program function
if __name__ == "__main__":
    main()
