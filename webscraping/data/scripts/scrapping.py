from bs4 import BeautifulSoup
import unicodedata
import re
import os
from .geolocator import get_cordinates
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .api_key import key
import time
import requests


def get_html(url):
    driver = webdriver.Chrome()  
    driver.get(url)
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            ver_mais_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Ver mais']")))
            ver_mais_button.click()
            time.sleep(3)

        except Exception as e:
            print("Não foi possível encontrar ou clicar no botão. Saindo do loop.")
            print(e)
            break

    html = driver.page_source

    with open('links.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    driver.quit()

    return html

def get_soup_html(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    return BeautifulSoup(html, 'html.parser')

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_links(soup):
    return [link.get('href') for link in soup.find_all('a', class_='StyledLink_styledLink__P_6FN')]

def clean_and_convert(value):
    value = unicodedata.normalize("NFKD", value).replace('\xa0', '')
    clean_value = re.sub(r'[^\d]', '', value)
    try:
        return int(clean_value)
    except ValueError:
        return None
    
def get_info(soup):
    meta_tag = soup.find('meta', attrs={'name': 'twitter:url'}).get('content')
    infos = [var.text for var in soup.find_all('p', class_='CozyTypography xih2fc EKXjIf Ci-jp3')]
    prices = [var.text for var in soup.find_all('div', class_='MuiBox-root mui-1ogb0fw')]
    location = soup.find('h4', class_='CozyTypography xih2fc EqjlRj').text + ', ' + soup.find('small', class_='CozyTypography xih2fc pwAPLE').text
    lat, long = get_cordinates(location,key)
    return {
        'ID': int(meta_tag.split('imovel/')[1].split('/', 1)[0]),
        'Location': location,
        'Lat': lat,
        'Long': long,
        'Square Meters': int(infos[0][0:2]),
        'Bedrooms': int(infos[1][0:1]),
        'Bathrooms': int(infos[2][0:1]),
        'Parking Spaces': [int(infos[3][0:1]) if infos[3][0:1] != '-' else 0][0],
        'Pets Allowed?': 1 if 'Aceita Pet' in infos[4] else 0,
        'Furnished?': 0 if 'Sem mobília' in infos[6] else 1,
        'Rent': clean_and_convert(prices[0].split('R$')[1]),
        'Condo Fee': clean_and_convert(prices[1].split('R$')[1]),
        'Property Tax': clean_and_convert(prices[2].split('R$')[1]),
        'Fire Insurance': clean_and_convert(prices[3].split('R$')[1]),
        'Service Tax': clean_and_convert(prices[4].split('R$')[1]),
        'Total': clean_and_convert(prices[5].split('R$')[1]),

    }




