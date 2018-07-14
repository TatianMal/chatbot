import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


class Parser:
    def __init__(self, url):
        self.html = ''
        self.get_html(url)

    def get_html(self, url):
        r = requests.get(url)
        self.html = r.text

    def get_news(self):
        soup = BeautifulSoup(self.html, 'lxml')
        wrap = soup.find('div', {'class': 'lent-left'})
        news = wrap.find_all('div', {'class': 'lent-block'})
        dict_news = OrderedDict()

        for new in news:
            try:
                header = new.find('div', {'class': 'title'})
                link = 'https://stopgame.ru' + header.find('a').get('href')
                header_text = header.text
            except Exception as e:
                print(e)
                dict_news['sorry'] = 'Извините, новостей не нашлось :('
                return dict_news

            dict_news[link] = header_text

        return dict_news


if __name__ == '__main__':
    par = Parser('https://stopgame.ru/news')
    print(par.get_news())