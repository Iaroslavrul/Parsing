from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import ssl
import time
import json

ssl._create_default_https_context = ssl._create_unverified_context
driver = webdriver.Chrome(ChromeDriverManager().install())


#1) открываю серп и чтобы получить доступ к вакансиям сначала нажимаю на кнопку, чтобы они подгрузилиль ajax-ом, после вызываю ф-ю для спора серпов
def getSerp()
    driver.get(httpsjobsearch.gov.aujobsearch)
    element = driver.find_element_by_class_name(job-search__button)
    element.click()
    getPages()


#3) обрабатываю page-и ф-ей, собираю из них данные, записываю их в словарь
def getData(url)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    all_text = driver.find_element_by_xpath('h1').text
    req_text = str.split(str(all_text), n)[0]
    position = req_text.replace(New, '')
    all_text = driver.find_element_by_class_name(map__link).text
    region = str.split(str(all_text), n)[0]
    desc = driver.find_element_by_id(job_description).text
    vacancys = {
        url url,
        position position,
        region region,
        desc desc
    }
    driver.quit()
    return vacancys


def writeToJson(vacancy_dict)
    try
        data = json.load(open('vacancys.json'))
    except
        data = []
    data.append(vacancy_dict)
    with open('vacancys.json', 'w') as file
        json.dump(data, file, indent=2, ensure_ascii=False)


#2) выхватываю ссылки вакансий по href и перехожу на них, вызывая для этого ф-ю getData, после отработки и возврата значений из getData записываю полученный словарь в json файл
def getPages()
    time.sleep(20)
    links = driver.find_elements_by_css_selector(a[href='JobViewDetails'])
    for link in links
        newPage = link.get_attribute(href)
        writeToJson(getData(newPage))


getSerp()
driver.close()