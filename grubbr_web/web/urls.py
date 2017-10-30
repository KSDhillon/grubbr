from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^meal/(?P<meal_id>[0-9]+)$', views.meal, name="meal"),
    url(r'^create/$', views.createMeal, name="create-meal"),
    url(r'^search/$', views.search_page, name="search"),
]
