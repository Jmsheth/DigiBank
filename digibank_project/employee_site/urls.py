from django.urls import path
from django.urls.conf import include
from . import views

app_name = "employee_site"
urlpatterns = [
    path('', views.index, name='emp-index'),
    path('login/', views.login, name='emp-login'),
]