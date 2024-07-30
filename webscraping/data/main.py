from scripts.scrapping import get_soup, get_links, get_info, get_soup_html
import pandas as pd

BASE_URL = 'https://www.quintoandar.com.br/alugar/imovel/belo-horizonte-mg-brasil'
BASE_HTML = 'links.html'

def main():
    ## Iniciar o processo de web scraping
    soup = get_soup_html(BASE_HTML)

    ## Pegar os links de cada apartamento da pagina HTML
    links = get_links(soup)

    ## Excract the info from all links and insert at a CSV
    for i, link in enumerate(links):
        try:
            soup = get_soup(link)
            info = get_info(soup)
            info = pd.DataFrame([info])
            info.to_csv(f'data.csv', mode='a', header=False, index=False)
            print(f'Inserindo {i+1} de {len(links)}')
        except:
            pass

if __name__ == "__main__":
    main()