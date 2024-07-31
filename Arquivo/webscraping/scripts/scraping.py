from bs4 import BeautifulSoup
import unicodedata
import re
from .geolocator import get_coordinates
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .api_key import key
import time
import requests


def fetch_html(url):
    """
    Abre uma página web usando Selenium e clica no botão "Ver mais" até que não haja mais botões para clicar.
    Salva o HTML da página em um arquivo.

    :param url: URL da página a ser carregada
    :return: HTML da página
    """
    driver = webdriver.Chrome()
    driver.get(url)
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            see_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Ver mais']")))
            see_more_button.click()
            time.sleep(3)
        except Exception as e:
            print("Não foi possível encontrar ou clicar no botão. Saindo do loop.")
            print(e)
            break

    html = driver.page_source

    with open('data/raw/links.html', 'w', encoding='utf-8') as file:
        file.write(html)

    driver.quit()
    return html


def parse_html_file(filename):
    """
    Lê um arquivo HTML e retorna um objeto BeautifulSoup.

    :param filename: Nome do arquivo HTML
    :return: Objeto BeautifulSoup
    """
    with open(filename, 'r', encoding='utf-8') as file:
        html = file.read()

    return BeautifulSoup(html, 'html.parser')


def fetch_soup(url):
    """
    Faz uma requisição GET a uma URL e retorna um objeto BeautifulSoup com o conteúdo da página.

    :param url: URL da página
    :return: Objeto BeautifulSoup
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def extract_links(soup):
    """
    Extrai todos os links de uma página HTML que possuem uma classe específica.

    :param soup: Objeto BeautifulSoup da página
    :return: Lista de links
    """
    return [link.get('href') for link in soup.find_all('a', class_='StyledLink_styledLink__P_6FN')]


def clean_and_convert(value):
    """
    Limpa e converte um valor string para um inteiro. Remove caracteres não numéricos.

    :param value: String a ser limpa e convertida
    :return: Valor inteiro ou None se a conversão falhar
    """
    normalized_value = unicodedata.normalize("NFKD", value).replace('\xa0', '')
    clean_value = re.sub(r'[^\d]', '', normalized_value)
    try:
        return int(clean_value)
    except ValueError:
        return None


def extract_info(soup):
    """
    Extrai informações de uma página HTML específica e retorna um dicionário com os dados.

    :param soup: Objeto BeautifulSoup da página
    :return: Dicionário com informações extraídas
    """
    meta_tag = soup.find('meta', attrs={'name': 'twitter:url'}).get('content')
    infos = [var.text for var in soup.find_all('p', class_='CozyTypography xih2fc EKXjIf Ci-jp3')]
    prices = [var.text for var in soup.find_all('div', class_='MuiBox-root mui-1ogb0fw')]
    location = f"{soup.find('h4', class_='CozyTypography xih2fc EqjlRj').text}, {soup.find('small', class_='CozyTypography xih2fc pwAPLE').text}"
    lat, lon = get_coordinates(location, key)
    return {
        'ID': int(meta_tag.split('imovel/')[1].split('/', 1)[0]),
        'Location': location,
        'Latitude': lat,
        'Longitude': lon,
        'Square Meters': int(infos[0][0:2]),
        'Bedrooms': int(infos[1][0:1]),
        'Bathrooms': int(infos[2][0:1]),
        'Parking Spaces': int(infos[3][0:1]) if infos[3][0:1] != '-' else 0,
        'Pets Allowed': 1 if 'Aceita Pet' in infos[4] else 0,
        'Furnished': 0 if 'Sem mobília' in infos[6] else 1,
        'Rent': clean_and_convert(prices[0].split('R$')[1]),
        'Condo Fee': clean_and_convert(prices[1].split('R$')[1]),
        'Property Tax': clean_and_convert(prices[2].split('R$')[1]),
        'Fire Insurance': clean_and_convert(prices[3].split('R$')[1]),
        'Service Tax': clean_and_convert(prices[4].split('R$')[1]),
        'Total': clean_and_convert(prices[5].split('R$')[1]),
    }
