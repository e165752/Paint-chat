# chat/urls.py
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^room/(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'^message/$', views.send_message, name='sendMessage'),
]
