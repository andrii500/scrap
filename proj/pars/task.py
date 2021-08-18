from random import randrange
from time import sleep
from celery import shared_task
from faker import Faker
from django.core.mail import send_mail
from .models import Page
import datetime as datetime


fake = Faker()


@shared_task
def create_random_students(total):
    result = []

    for _ in range(total):
        result.append(Page(
            link='https://forklog.com/s-nachala-goda-eksperty-obnaruzhili-bolee-1500-moshennicheskih-sajtov-natselennyh-na-kriptoinvestorov/',
            title='С начала года эксперты обнаружили более 1500 мошеннических сайтов, нацеленных на криптоинвесторов',
            article_author='Каролина Сэлинджер',
            pub_date=datetime.datetime.strptime('18.08.2021', '%d.%m.%Y').date(),
            tags='#лаборатория касперского#мошенничество',
            text='С января 2021 года специалисты «Лаборатории Касперского» зафиксировали более 1500 мошеннических ресурсов, направленных на криптовалютных инвесторов и заинтересованных в майнинге пользователей.'
        ))
    Page.objects.bulk_create(result)

    return 'Pages write in base.'


@shared_task
def beat():
    print('beat START')
    sleep(5)
    print('beat END')
