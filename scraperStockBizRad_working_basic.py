import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Set up the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')  # optional: run in headless mode
driver = webdriver.Chrome(options=options)
url_to_search = "https://www.biznesradar.pl/notowania-historyczne/DBE"


def scrape_data(url):
    driver.get(url)
    time.sleep(1)  # wait for page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_rows = soup.find_all('tr')

    for row in table_rows:
        cols = row.find_all('td')
        if cols:
            cols = [col.text.strip() for col in cols]
            print(', '.join(cols))

scrape_data(url_to_search)


driver.quit()