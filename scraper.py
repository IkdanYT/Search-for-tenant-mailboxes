import json
from datetime import datetime
import io
import random
import re
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv

# Changing the default input/output encoding to UTF-8 | Изменение стандартной кодировки ввода/вывода на UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def random_sleep(minimum, maximum):
    """Sleep between minimum and maximum seconds. | Спать между minimum и maximum секундами."""
    time.sleep(random.uniform(minimum, maximum))

def create_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Work in headless mode for improved performance | Работать в режиме headless для улучшения производительности
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    service = Service(executable_path=r'D:\Загрузки\chromedriver.exe') # Path to ChromeDriver.exe | Путь до ChromeDriver.exe
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def google_search_for_emails(driver, query):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query + " email")
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    email_addresses = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text()))
    return list(email_addresses)

def save_to_csv(data, filename):
    """Saving data to CSV. | Сохранение данных в CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["number", "title", "description", "emails"])
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def save_to_json(data, filename):
    """Saving data to JSON. | Сохранение данных в JSON."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def find_elements(soup, selector):
    return soup.select(selector) if selector.startswith('.') else soup.find_all(selector)

def get_company_info_from_page(soup, selector_info, count):
    company_info = []
    # Avoid the item search operation if the container selector is not represented | Избегаем операции поиска элементов, если селектор контейнера не представлен
    if "container" in selector_info:
        elements = soup.select(selector_info["container"])
    else:  # If there is no container selector, assume that the entire page contains data | Если селектор контейнера отсутствует, предполагаем, что все страница содержит данные
        elements = [soup]
    
    for element in elements:
        title_element = element.select_one(selector_info['title']) if "title" in selector_info else None
        desc_element = element.select_one(selector_info['desc']) if "desc" in selector_info else None
        
        # Checking for a header to continue the email search | Проверка наличия заголовка для продолжения поиска email
        if not title_element:
            continue
        
        title = title_element.get_text().strip() if title_element else 'No Header | Нет Заголовка'
        desc = desc_element.get_text().strip() if desc_element else 'No Description | Нет Описания'
        
        random_sleep(0.5, 2.0)
        emails = google_search_for_emails(driver, title) if title != 'No Header | Нет Заголовка' else ['Title not found | Заголовок не найден']
        
        count += 1
        result = {
            "number": count,
            "title": title,
            "description": desc,
            "emails": emails
        }
        company_info.append(result)
        print(json.dumps(result, ensure_ascii=False))  # Printing information in JSON format | Печать информации в JSON формате
        
    return company_info, count

driver = create_chrome_driver()
data_to_export = []  # List for saving results | Список для сохранения результатов

try:
    tower_urls = [
        {
            "url": "https://federation.moscow-city-towers.ru/all_arends", 
            "selector": { "container": ".content", "title": "h4", "desc": "span" }
        },
        {
            "url": "https://mercury.moscow-city-towers.ru/spisarend",
            "selector": { "container": ".content", "title": "h4", "desc": "span" }
        },
        {
            "url": "https://www.eurasia-city-tower.ru/spisarend",
            "selector": { "container": ".content", "title": "h4", "desc": "span" }
        },
        {
            "url": "https://north.moscow-city-towers.ru/all_arends",
            "selector": { "container": ".content", "title": "h4", "desc": "span" }
        },
        {
            "url": "https://empire-city-tower.ru/spisarend",
            "selector": { "container": ".content", "title": "h2", "desc": "p" }
        },
        {
            "url": "https://fortexgroup.ru/bc/bashnya-na-naberezhnoy/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        },
        {
            "url": "https://fortexgroup.ru/bc/bashnya-evolyutsiya/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        },
        {
            "url": "https://fortexgroup.ru/bc/bashnya-federatsiya/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        },
        {
            "url": "https://fortexgroup.ru/bc/merkuriy-15693/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        },
        {
            "url": "https://fortexgroup.ru/bc/severnaya-bashnya/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        },
        {
            "url": "https://fortexgroup.ru/bc/imperiya-tauer/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        },
        {
            "url": "https://fortexgroup.ru/bc/gorod-stolits/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        },
        {
            "url": "https://fortexgroup.ru/bc/park-tauer-2930/arendatory/",
            "selector": { "container": ".famousTenants__item", "title": ".tenantItem__name", "desc": ".tenantItem__category" }
        }
    ]

    count = 0
    for tower in tower_urls:
        driver.get(tower["url"])
        container_selector = tower["selector"]["container"]
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, container_selector)))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        info, count = get_company_info_from_page(soup, tower["selector"], count)
        data_to_export.extend(info)

    # Getting the current date for file names | Получение текущей даты для имен файлов
    date_string = datetime.now().strftime("%d_%m_%Y")
    json_filename = f"result_{date_string}.json"
    csv_filename = f"result_{date_string}.csv"
    
    # Save data to JSON | Сохраняем данные в JSON
    save_to_json(data_to_export, json_filename)
    
    # Saving data to CSV | Сохраняем данные в CSV
    save_to_csv(data_to_export, csv_filename)

except Exception as e:
    print(f"There's been an error | Произошла ошибка: {e}")

finally:
    driver.quit()