from scripts.scraping import fetch_soup, extract_links, extract_info, parse_html_file, fetch_html
from config.vars import BASE_HTML, BASE_URL
import pandas as pd

def main():
    """
    Função principal que orquestra o processo de web scraping e salva os dados extraídos em um arquivo CSV.
    """
    # Pegar o HTML da página principal e salvar
    html = fetch_html(BASE_URL)

    # Iniciar o processo de web scraping
    soup = parse_html_file(BASE_HTML)

    # Pegar os links de cada apartamento da página HTML
    links = extract_links(soup)

    # Extrair as informações de todos os links e inserir em um CSV
    for i, link in enumerate(links):
        try:
            soup = fetch_soup(link)
            info = extract_info(soup)
            info_df = pd.DataFrame([info])
            info_df.to_csv('data/processed/data.csv', mode='a', header=False, index=False)
            print(f'Inserindo {i + 1} de {len(links)}')
        except Exception as e:
            print(f'Erro ao processar o link {link}: {e}')
            continue

if __name__ == "__main__":
    main()
