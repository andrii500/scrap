import requests
from bs4 import BeautifulSoup


def get_news_links(num_of_page):
    url = 'https://forklog.com/news/page/'
    links_list = []

    for page in range(1, num_of_page + 1):
        r = requests.get(f"{url}{str(page)}/")
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all('div', {'class': 'post_item'})

        for link in divs:
            link = link.find('a').get('href')
            if link not in links_list:
                links_list.append(link)

    return links_list


def parse_new_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    title = soup.find('h1').get_text()
    article_date = soup.find('span', {'class': 'article_date'}).get_text()
    article_author = soup.find('a', {'class': 'article_author'}).get_text()

    post_tags = soup.find('div', {'class': 'post_tags_top'}).find_all('a')
    tags_text = ''
    for tag in post_tags:
        tags_text += tag.get_text()

    ps_text = soup.find('div', {'class': 'post_content'}).find_all('p')
    topic_text = ''
    for p in ps_text:
        topic_text += p.get_text() + '\n'

    return title, article_author, article_date, tags_text, topic_text


# topic_list = []
#
# for link in get_news_links(1):
#     topic_list.append(parse_new_page(link))
#
#
# with open('example.txt', 'a+') as f:
#     for topic in topic_list:
#         f.write(str(topic) + '\n')


def parse_new_page_test(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    text = soup.find('div', {'class': 'post_content'}).get_text()

    return text


print(parse_new_page_test(
    'https://forklog.com/smi-minfin-ssha-opublikuet-rukovodstvo-po-nalogooblozheniyu-kriptokompanij/'))
