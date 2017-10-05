from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^meal/(?P<meal_id>[0-9]+)$', views.meal, name="meal"),
]
