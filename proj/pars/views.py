from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup


def index(request):
    return HttpResponse('Hello world')


def parse(request):
    url = 'https://forklog.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    divs = soup.find_all('div', {'class': 'post_item'})
    news_links = []
    for link in divs:
        link = link.find('a').get('href')
        news_links.append(link)
    return HttpResponse(f"{news_links}")

# def parse():
#     url = 'https://forklog.com/news/'
#     r = requests.get(url)
#     #print(r.text)
#     soup = BeautifulSoup(r.text)
#     divs = soup.find_all('div', {'class': 'post_item'})
#     news_links = []
#     for link in divs:
#         link = link.find('a').get('href')
#         news_links.append(link)
#     num = 0
#     for i in news_links:
#         num += 1
#         print(i)
#     print(num)
#
# parse()

