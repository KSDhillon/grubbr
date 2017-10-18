from django.conf.urls import include, url
from .services import *

urlpatterns = [
    url(r'^meals/$', get_home_page, name='homepage'),
    url(r'^meal/(?P<meal_id>[0-9]+)$', get_detail_page , name='detail'),
]
