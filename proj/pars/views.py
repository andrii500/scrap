from django.shortcuts import render
from django.http import HttpResponse
from .models import Page
from .task import parse_pages


def get_pages(request):
    parse_pages.delay()
    pages = Page.objects.all()[0:10]
    return render(request, 'index.html', {'pages': pages})


def get_page(request, page_id):
    page = Page.objects.filter(id=page_id).first()
    return render(request, 'page.html', {'page': page})
