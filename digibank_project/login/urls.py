from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.i18n import urlpatterns
from . import views
from django.urls import path
app_name="login"

urlpatterns = [
    path('', views.login, name='login'),
    '''
    
    '''
]