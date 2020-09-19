from selenium import webdriver
import xlsxwriter
import time
import random

def open_web_driver():
    driver = webdriver.Edge()
    return driver

def open_web_page():
    #global driver
    driver.get("http://corpus.rae.es/creanet.html")
    driver.implicitly_wait(10)

def make_consulta(lexeme, autor, year1, year2, obra, medio, country, tema):
    #global driver
    #Locate the elements in the webpage using their names or xpaths
    consulta = driver.find_element_by_name("texto")
    consulta.send_keys(lexeme)

    #Add criterios de seleccion if any
    if autor != "" and autor != " ":
        author_name = driver.find_element_by_name("autor")
        author_name.send_keys(autor)
    if year1 != "" and year1 != " ":
        cronologico_start = driver.find_element_by_name("ano1")
        cronologico_start.send_keys(year1)
    if year2 != "" and year2 != " ":
        cronologico_end = driver.find_element_by_name("ano2")
        cronologico_end.send_keys(year2)
    if obra != "" and obra != " ":
        obra_s_title = driver.find_element_by_name("titulo")
        obra_s_title.send_keys(obra)

    #Select the specified options from the menus (medio, geografico, and tema ) if any
    if medio != "Elegir" and medio != "(Todos)":
        type_publication = driver.find_element_by_xpath(f"/html/body/blockquote/form/div/table/tbody/tr[4]/td[4]/p/select/option[contains(text(), '{medio}')]").click()
    if country != "Elegir" and country != "(Todos)":
        geografico = driver.find_element_by_xpath(f"/html/body/blockquote/form/div/table/tbody/tr[4]/td[6]/p/select/option[contains(text(), '{country}')]").click()
    if tema != "Elegir" and country != "(Todos)":
        topic = driver.find_element_by_xpath(f"/html/body/blockquote/form/div/table/tbody/tr[5]/td[2]/p/select/option[contains(text(), '{tema}')]").click()


    #Click search
    search_button = driver.find_element_by_xpath("/html/body/blockquote/form/p/span/input[1]").click()
    driver.implicitly_wait(15)

    #Click "Recuperar" sentences
    try:
        recuperar_button = driver.find_element_by_xpath("/html/body/blockquote/table[4]/tbody/tr[2]/td[1]/input").click()
        driver.implicitly_wait(10)
    except:
        try:
            number_of_results = driver.find_element_by_xpath("/html/body/blockquote/table[2]/tbody/tr[4]/td[2]/span").text
            print(f'We found {number_of_results} That\'s way too many examples! Narrow down your search or search for a different word!')
            driver.quit()
            return True
        except:
            print("No matches found for your search. Please check the spelling")
            driver.quit()
            return False

def get_number_of_instances( my_number):
    #global driver
    driver.implicitly_wait(10)
    txt = driver.find_element_by_xpath("/html/body/blockquote/center/table[1]/tbody/tr[3]/td[2]/span").text
    txt = txt.split()
    if int(my_number) < int(txt[0]):
        return my_number
    else:
        return int(txt[0])

def gather_and_save_all_info(word, number):
    #global driver
    #Get generic href
    driver.implicitly_wait(10)
    generic_link = driver.find_element_by_xpath("/html/body/blockquote/center/pre/tt/a[1]").get_attribute('href')
    driver.implicitly_wait(10)

    #Create an excel file
    workbook = xlsxwriter.Workbook(f'{word}_data.xlsx', {'strings_to_urls':False})
    worksheet = workbook.add_worksheet('sentences')

    #Add headers in bold letters to excel file
    headers = ['Sentence', 'Link', 'Year', 'Author', 'Title', 'Country', 'Topic', 'Publication']
    header_format = workbook.add_format({'bold':True})
    worksheet.write_row('A1', headers, header_format)

    #Create and set column and text formats
    general_format = workbook.add_format({'text_wrap':1, 'valign':'top'})
    url_format = workbook.add_format({'valign':'top'})
    year_format = workbook.add_format({'text_wrap':1, 'align':'left', 'valign':'top'})
    concept_format = workbook.add_format({'bold':True, 'font_color':'#8b1728', 'italic':True, 'underline':True})
    worksheet.set_column('A:A', 50, general_format)
    worksheet.set_column('E:E', 20, general_format)
    worksheet.set_column('G:G', 20, general_format)
    worksheet.set_column('H:H', 25, general_format)

    row_number = 2

    #Fetch every example in the page, example by example
    for i in range(number):
        #Go to every link
        seconds = 5 + (random.random() * 5)
        time.sleep(seconds)
        formated_string = f'iniItem={i}'
        active_url = generic_link.replace("iniItem=0", formated_string)
        driver.get(active_url)
        driver.implicitly_wait(10)

        #Locate the paragraph where the word appears using beautifulSoup and requests
        driver.get(active_url)
        driver.implicitly_wait(15)
##################################
        try:
            txt = driver.find_element_by_xpath(f'//font[contains(text(), "{word}")]/ancestor::p').text
        except:
            txt = driver.find_element_by_xpath(f'//font[contains(text(), "{word}")]/ancestor::td').text

        #Split the text in three parts to add format to the word looked up
        part1 = "'" + txt.split(word, 1)[0]
        part2 = "'" + txt.split(word, 1)[1]

        #Find the rest of the elements we need
        driver.implicitly_wait(10)
        year = driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[1]/td[2]").text
        author = driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[2]/td[2]").text
        title = driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[3]/td[2]").text
        country = driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[4]/td[2]").text
        topic = driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[5]/td[2]").text
        publication = driver.find_element_by_xpath("/html/body/blockquote/table[3]/tbody/tr[6]/td[2]").text

        #Modify url to avoid \000 elimination
        #url = href.replace('\000', '\\000')

        #Add information to worksheet
        worksheet.write_rich_string(f'A{row_number}', part1, concept_format, word, part2)
        worksheet.write_string(f'B{row_number}', active_url, url_format)
        worksheet.write(f'C{row_number}', year, year_format)
        worksheet.write(f'D{row_number}', author, general_format)
        worksheet.write(f'E{row_number}', title, general_format)
        worksheet.write(f'F{row_number}', country, general_format)
        worksheet.write(f'G{row_number}', topic, general_format)
        worksheet.write(f'H{row_number}', publication, general_format)
        row_number += 1

    workbook.close()
    driver.quit()



if __name__ == "__main__":
    #Here we run everything!!
    concept = 'chayote'
    driver = open_web_driver()
    open_web_page()
    #             lexeme, autor, year1, year2, obra, medio, country, tema
    make_consulta(concept, "", "", "", "", "", "", "2.- Ciencias sociales, creencias y pensamiento.")
    number_of_sentences = get_number_of_instances(5)
    gather_and_save_all_info(concept, number_of_sentences)
