from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select

data = {'texto': 'uva',
        'autor': 'Pirolo',
        'ano1': '1985',
        'ano2': '',
        'titulo': 'El libro de las dietas',
        'medio': '',
        'pais': 'ARGENTINA',
        'tema': '501.- Gastronomía'
        }

def check_parameters(data):
    for parameter in data:
        parameter = driver.find_element_by_name(parameter)

def make_consulta(driver=None, data=None):
    driver = webdriver.Edge()
    driver.get('http://corpus.rae.es/creanet.html')

    tema = Select(driver.find_element_by_name("tema"))
    tema.select_by_visible_text('101.- Biología.')

    #driver.quit()

make_consulta()
"""
    driver = webdriver.Edge()
    try:
        driver.get("https://www.google.com")
    except WebDriverException as exception:
        print("You closed it!")
"""
