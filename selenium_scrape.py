from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
from configparser import ConfigParser

# Uses Selenium to get the top result in 'Most Popular Places at this Location' subsection
# Takes a while tho
# Enter the path to your chromedriver.exe file in the service variable
# HELPER FUNCTION FOR REPLACE_ADDRESS()
def selenium_scrape(expanded_address: str):
    # Read from config
    main_config = ConfigParser()
    main_config.read('config.ini')

    TARGET_CLASS = 'fpqsoc'

    # prepare a google search url for a request
    url = 'https://www.google.com/search?q=' + expanded_address.replace(' ', '+')

    # Set up Selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    #Set User Agent so Google doesn't know we are scraping/automating.
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Get the page and wait for the js to run
    driver.get(url)
    wait = WebDriverWait(driver, 8)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, TARGET_CLASS)))
    except:
        return None

    # Get the new HTML after the js has run
    html = driver.page_source
    driver.quit()

    # Now we can parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all(class_=TARGET_CLASS)

    return results[0].text