from django.urls import path
from . import views


urlpatterns = [
    path('', views.parse_pages, name='parse-pages'),
    path('page/<int:page_id>', views.get_page, name='get-page'),
]
