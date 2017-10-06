from django.conf.urls import include, url
from .services import *

urlpatterns = [
    url(r'^meals/$', get_meals, name='meal_list'),
    url(r'^meal/(?P<meal_id>[0-9]+)$', get_meal , name='meal'),
]
