import json
import requests
from bs4 import BeautifulSoup


def get_quotes():
    max_pages = 10
    page = 0
    quotes = []
    authors = {}
    while page < max_pages:
        page += 1
        try:
            url = 'https://quotes.toscrape.com/page/' + str(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            for i in range(len(soup.find_all('span', class_='text'))):
                quote = soup.find_all('span', class_='text')[i].text
                author_el = soup.find_all('small', class_='author')[i]
                author = author_el.text
                author_url = author_el.find_next_sibling('a').attrs['href']

                if author_url not in authors:
                    authors[author_url] = scrape_author(author_url)

                tags_list = soup.find_all('div', class_='tags')[i].find_all('a', class_='tag')
                tags = [tag.text for tag in tags_list]
                quotes.append({"tags": tags, "author": author, "quote": quote})

        except Exception as ex:
            print(ex)
            print("probably last page:", page)
            break


    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(quotes, fd, ensure_ascii=False, indent=4)

    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(list(authors.values()), fd, ensure_ascii=False, indent=4)


def scrape_author(author_url: str):
    url = 'http://quotes.toscrape.com/' + author_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    author_info = {
        "fullname": soup.select_one(".author-title").text.strip(),
        "born_date": soup.select_one(".author-born-date").text.strip(),
        "born_location": soup.select_one(".author-born-location").text.strip(),
        "description": soup.select_one(".author-description").text.strip()
    }
    return author_info


if __name__ == '__main__':
   get_quotes()