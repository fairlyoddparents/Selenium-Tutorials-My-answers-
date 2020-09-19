from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

def lets_open_selenium():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://stackoverflow.com/questions/37693372/wait-a-process-to-finish-in-python-script")
    element = driver.find_element_by_id("question-header")
    print(element.text)
    driver.quit()

lets_open_selenium()
