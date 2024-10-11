from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import os
import time
import csv

# Create a new instance of FirefoxOptions
options = Options()

# Set up Firefox driver in headless mode
driver = webdriver.Firefox(options=options)

url_to_search = "https://www.biznesradar.pl/notowania-historyczne/DBE"

def scrape_data(url, is_first_page):
    # Navigate to the specified URL
    driver.get(url)

    # Wait for the page to load
    time.sleep(2)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table with class "qTableFull"
    table = soup.find('table', {'class': 'qTableFull'})

    if table is not None:
        print(f"Table found on {url}!")
        # Extract data from the table
        rows = table.find_all('tr')
        
        # Open the CSV file in append mode ('a') if it's not the first page, otherwise in write mode ('w')
        mode = 'w' if is_first_page else 'a'
        with open('scraped_data.csv', mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write the header only for the first page
            if is_first_page:
                writer.writerow(['Data', 'Otwarcie', 'Max', 'Min', 'Zamknięcie', 'Wolumen', 'Obrót'])
            
            # Write the data rows
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if len(cols) == 7:  # Ensure we have all 7 columns
                    data = [col.text.strip() for col in cols]
                    writer.writerow(data)
    else:
        print(f"Table not found on {url}!")

# Scrape data from all pages
for i in range(0, 5):  # Increased range to 5 pages for this example
    url_to_search_iterate = url_to_search + f",{i}"
    scrape_data(url_to_search_iterate, is_first_page=(i == 0))

driver.quit()