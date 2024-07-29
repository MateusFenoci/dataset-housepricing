from bs4 import BeautifulSoup
import unicodedata
import re
from .geolocator import get_cordinates
import requests

BASE_URL = 'https://www.quintoandar.com.br/alugar/imovel/belo-horizonte-mg-brasil?pagina='

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def generate_urls(n_pages):
    return [BASE_URL + str(page) for page in range(1, n_pages + 1)]

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
    infos = [var.text for var in soup.find_all('p', class_='CozyTypography xih2fc EKXjIf Ci-jp3')]
    prices = [var.text for var in soup.find_all('div', class_='MuiBox-root mui-1ogb0fw')]
    location = soup.find('h4', class_='CozyTypography xih2fc EqjlRj').text + ', ' + soup.find('small', class_='CozyTypography xih2fc pwAPLE').text
    ##lat, long = get_cordinates(location)
    return {
        'Square Meters': int(infos[0][0:2]),
        'Bedrooms': int(infos[1][0:1]),
        'Bathrooms': int(infos[2][0:1]),
        'Parking Spaces': int(infos[3][0:1]),
        'Pets Allowed?': 1 if 'Aceita Pet' in infos[4] else 0,
        'Furnished?': 0 if 'Sem mobília' in infos[6] else 1,
        'Rent': clean_and_convert(prices[0].split('R$')[1]),
        'Condo Fee': clean_and_convert(prices[1].split('R$')[1]),
        'Property Tax': clean_and_convert(prices[2].split('R$')[1]),
        'Fire Insurance': clean_and_convert(prices[3].split('R$')[1]),
        'Service Tax': clean_and_convert(prices[4].split('R$')[1]),
        'Total': clean_and_convert(prices[5].split('R$')[1]),
        'Location': location,
    }
