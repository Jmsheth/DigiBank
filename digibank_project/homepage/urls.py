from django.urls import path
from django.urls.conf import include
from . import views

app_name = "homepage"
urlpatterns = [
    path('', views.index, name='index'),
]