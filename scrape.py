import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Constants
DRIVER_PATH = "/usr/bin/chromedriver"
BASE_DIR = os.path.dirname(__file__)
INIT_URL = "https://www.huskermax.com/statistics/2019-nebraska-football-statistics/"

# Make data folder
DATA_FOLDER = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_FOLDER, exist_ok=True)

# PDF - /html/body/div[3]/main/article/div[1]/div[3]/iframe
# Text - /html/body/div[3]/main/article/div[1]/div[2]/iframe

def change_year(driver, decade_idx, year_idx):
    # action chains to provide mouse movement/events
    action = ActionChains(driver)
    # dropdown is located within this iframe --> need to switch to it and perform actions within it
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@src=\"/stats/navStats.html\"]"))
    # navigate to menu -> submenus and click
    firstLevelMenu = driver.find_element_by_xpath("//*[@id=\"navHmx\"]") # main menu
    action.move_to_element(firstLevelMenu).perform()
    secondLevelMenu = driver.find_element_by_xpath(f"//*[@id=\"navHmx\"]/li/ul/li[{decade_idx}]") # decade
    action.move_to_element(secondLevelMenu).perform()
    thirdLevelMenu = driver.find_element_by_xpath(f"//*[@id=\"navHmx\"]/li/ul/li[{decade_idx}]/ul/li[{year_idx}]") # year
    action.move_to_element(thirdLevelMenu).perform()
    thirdLevelMenu.click()

def get_data(driver, year):
    # update output files
    pdfpath = os.path.join("data", "pdfstats.txt")
    filepath = os.path.join("data", f"{year}.txt")
    raw_data = driver.find_elements_by_tag_name("pre")

    if len(raw_data) == 0: #aka - data is hosted in PDF
        with open(pdfpath, 'a') as file:
            file.write(f"{year}\n")
    else:
        with open(filepath, 'a') as file: #success - data is accessible
            for data in raw_data:
                file.write(data.get_attribute("textContent")) # have to use .get_attribute("textContent") instead of .text because raw_data[3] is hidden on most pages    

def run(year, decade_idx, year_idx):
    driver = webdriver.Chrome(DRIVER_PATH)

    driver.get(INIT_URL)
    driver.maximize_window()
    time.sleep(5) # sleep so page can load properly
    
    while year >= 1962:
        get_data(driver, year)
        year_idx += 1
        if year_idx == 11:
            decade_idx += 1
            year_idx = 1
        change_year(driver, decade_idx, year_idx)
        year -= 1
        time.sleep(5)

if __name__ == "__main__":
    # Initializations
    year = 2019 # start from 2019 and work back to 1962
    decade_idx = 1 # index of 2010s
    year_idx = 1 # top year of decade, e.g. index of 2019
    run(year, decade_idx, year_idx)
    driver.quit()