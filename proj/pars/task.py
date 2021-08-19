from celery import shared_task
from .models import Page
import requests
from bs4 import BeautifulSoup
import datetime as datetime


@shared_task
def parse_pages():
    url = 'https://forklog.com/news/page/'
    page_num = 1

    while True:
        if requests.get(f"{url}{page_num}"):
            r = requests.get(f"{url}{str(page_num)}/")
            soup = BeautifulSoup(r.text, features="html.parser")
            divs = soup.find_all('div', {'class': 'post_item'})

            for link in divs:
                link = link.find('a').get('href')
                parse_page(link)
            page_num += 1
        else:
            break


def parse_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    if not soup.find('div', {'class': 'deleted_post_disclamer'}):
        title = soup.find('h1').get_text()
        pub_date_ = soup.find('span', {'class': 'article_date'}).get_text()
        pub_date = datetime.datetime.strptime(pub_date_, '%d.%m.%Y').date()
        article_author = soup.find('a', {'class': 'article_author'}).get_text()

        if soup.find('div', {'class': 'post_tags_top'}):
            post_tags = soup.find('div', {'class': 'post_tags_top'}).find_all('a')
            tags = ''
            for tag in post_tags:
                tags += tag.get_text()
        else:
            tags = ''

        text = soup.find('div', {'class': 'post_content'}).get_text()
        text = text.replace(title, '')
        text = text.replace(pub_date_, '')
        text = text.replace(article_author, '')
        text = text.replace(tags, '')
        text = text.replace('Нашли ошибку в тексте? Выделите ее и нажмите CTRL+ENTER', '')
        text = text.strip('\n')

        if not Page.objects.filter(link=url).exists():
            Page.objects.create(link=url, title=title, article_author=article_author, pub_date=pub_date, tags=tags, text=text)
