# chat/urls.py
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.__exp_rest__, name='__exp_rest__'),
    path('forecast', views.forecast, name='forecast'),    
]
