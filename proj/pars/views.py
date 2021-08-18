from django.shortcuts import render
from django.http import HttpResponse
from .models import Page

import requests
from bs4 import BeautifulSoup
import datetime as datetime


def get_news_links():
    url = 'https://forklog.com/news/page/'
    page_num = 1
    links_list = []

    while True:
    # for i in [1, 2]:
        if requests.get(f"{url}{page_num}"):
            r = requests.get(f"{url}{str(page_num)}/")
            soup = BeautifulSoup(r.text, features="html.parser")
            divs = soup.find_all('div', {'class': 'post_item'})

            for link in divs:
                link = link.find('a').get('href')
                if link not in links_list:
                    links_list.append(link)
            page_num += 1
        else:
            break
    # 25830
    return links_list


def parse_page(request, url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    if soup.find('h1'):
        title = soup.find('h1').get_text()
    else:
        title = ''

    if soup.find('span', {'class': 'article_date'}):
        pub_date_ = soup.find('span', {'class': 'article_date'}).get_text()
        pub_date = datetime.datetime.strptime(pub_date_, '%d.%m.%Y').date()
    else:
        pub_date_ = ''
        pub_date = ''

    if soup.find('a', {'class': 'article_author'}):
        article_author = soup.find('a', {'class': 'article_author'}).get_text()
    else:
        article_author = ''

    post_tags = ''
    if soup.find('div', {'class': 'post_tags_top'}):
        post_tags = soup.find('div', {'class': 'post_tags_top'}).find_all('a')

    tags = ''
    for tag in post_tags:
        tags += tag.get_text()

    text = soup.find('div', {'class': 'post_content'}).get_text()

    text = text.replace(title, '')
    text = text.replace(pub_date_, '')
    text = text.replace(article_author, '')
    text = text.replace(tags, '')
    text = text.replace('Нашли ошибку в тексте? Выделите ее и нажмите CTRL+ENTER', '')
    text = text.strip('\n')

    if not Page.objects.filter(link=url).exists():
        Page.objects.create(link=url, title=title, article_author=article_author, pub_date=pub_date, tags=tags, text=text)


def parse_pages(request):
    links_list = get_news_links()

    for link in links_list:
        parse_page(request, link)

    pages = Page.objects.all()
    return render(request, 'index.html', {'pages': pages})


def get_page(request, page_id):
    page = Page.objects.filter(id=page_id).first()
    return render(request, 'page.html', {'page': page})
