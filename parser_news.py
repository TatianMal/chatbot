import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


class Parser:
    def __init__(self, base_url, name_game):
        self.html = ''
        self.url = self. make_final_url(base_url, name_game)
        self.get_html()

    def make_final_url(self, base_url, name_game):
        if name_game != '':
            tmp_name = name_game.split(' ')
            tmp_url = base_url + 'search/?s=' + tmp_name[0]
            for part in range(len(tmp_name)):
                if part == 0:
                    continue
                else:
                    tmp_url += '+' + tmp_name[part]
            tmp_url += '&where=news'
            return tmp_url
        else:
            return base_url + 'news'

    def get_html(self):
        r = requests.get(self.url)
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
    par = Parser('https://stopgame.ru/', '')
    print(par.get_news())