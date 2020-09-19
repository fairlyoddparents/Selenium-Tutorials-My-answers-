from selenium import webdriver
from selenium.common.exceptions import WebDriverException

driver = webdriver.Edge()
try:
    driver.get("https://www.google.com")
except WebDriverException as exception:
    print("You closed it!")
