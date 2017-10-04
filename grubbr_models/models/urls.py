from django.conf.urls import include, url
from .services import *

urlpatterns = [
    url(r'^user/$', create_user),
    url(r'^meal/$', create_meal),
    url(r'^user/(?P<user_id>[0-9]+)$', rud_user_by_id),
    url(r'^meal/(?P<meal_id>[0-9]+)$', rud_meal_by_id),
]
