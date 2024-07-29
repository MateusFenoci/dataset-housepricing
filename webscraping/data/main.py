from scripts.scrapping import get_soup, generate_urls, get_links, get_info

def main():

    ## Nº of pages to scrape
    urls = generate_urls(1)

    ## List of links from all pages
    links = []
    for url in urls:
        soup = get_soup(url)
        links.extend(get_links(soup))

    ## Excract the info from all links
    for link in links:
        soup = get_soup(link)
        info = get_info(soup)

        print(info)
        break


if __name__ == "__main__":
    main()