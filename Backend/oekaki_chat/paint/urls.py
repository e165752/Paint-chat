# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.canvas, name='canvas'),
    url(r'^chat/(?P<room_name>[^/]+)/$', views.canvas, name='canvas'),
    url(r'^receive/$', views.receiveAndSendJPG, name='receiveAndSendJPG'),
]
