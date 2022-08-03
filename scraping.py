import requests
import bs4
from datetime import datetime


def get_title(article):
    article_tag_span = article.find('h2').find('a').find('span')
    return article_tag_span.text


def get_time(article):
    article_tag = article.find('span', class_='tm-article-snippet__datetime-published')
    article_tag_time = article_tag.find('time')
    str_time = article_tag_time.attrs['title']
    return datetime.strptime(str_time, '%Y-%m-%d, %H:%M')


def get_url(article):
    article_tag_a = article.find('h2').find('a')
    href = article_tag_a.attrs['href']
    return 'https://habr.com' + href


def filter_article(words, url):
    article_response = requests.get(url)
    article_code = article_response.text
    article_soap = bs4.BeautifulSoup(article_code, features='html.parser')
    article_tag = article_soap.find('div', class_='tm-article-body')
    for word in words:
      if word in article_tag.text:
        return True
    return False


if __name__ == '__main__':
    KEYWORDS = ['фото', 'python', 'web']
    print('Ищу подходящие статьи...')
    response = requests.get('https://habr.com/ru/all/')
    text = response.text

    soap = bs4.BeautifulSoup(text, features='html.parser')
    articles = soap.find_all('article', class_='tm-articles-list__item')

    for article in articles:
        title = get_title(article)
        time = get_time(article)
        url = get_url(article)
        if filter_article(KEYWORDS, url):
            print(time.strftime('%d.%m.%Y'), '////', title, '////', url)

    print('Поиск окончен')
