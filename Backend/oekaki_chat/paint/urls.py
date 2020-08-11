# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.canvas, name='canvas'),
    url(r'^chat/room/(?P<room_name>[^/]+)/$', views.canvas, name='canvas'),
    # JS からの post を受ける時は、CSFR_token 設定が必要で、その時に form で引数の指定が必要になるので、request しか実質使えない...。
    url(r'^receive/$', views.receiveAndSendJPG, name='receiveAndSendJPG'),
]
