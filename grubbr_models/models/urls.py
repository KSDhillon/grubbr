from django.conf.urls import include, url
from .services import *

urlpatterns = [
    url(r'^register/$', create_user, name='user_create'),
    url(r'^meal/$', create_meal, name='meal_create'),
    url(r'^login/$', login_user, name='login_user'),
    url(r'^user/(?P<user_id>[0-9]+)$', rud_user_by_id, name='user_action'),
    url(r'^meal/(?P<meal_id>[0-9]+)$', rud_meal_by_id, name='meal_action'),
]
