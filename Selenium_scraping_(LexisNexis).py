from selenium import webdriver

driver = webdriver.Edge()
driver.get("https://scholar.google.com.mx/")
#driver.switch_to_frame('mainFrame')
balloon = driver.find_element_by_id('gs_hdr_tsi')
balloon.clear()
balloon.send_keys('balloon')
search_button = driver.find_element_by_xpath('//*[@id="gs_hdr_tsb"]').click()
