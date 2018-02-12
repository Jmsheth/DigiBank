from django.urls import path
from django.urls.conf import include
from . import views

app_name = "employee_site"
urlpatterns = [
    path("account_activation/",
         views.emp_account_act,
         name="account activation"),
    path("dd_req/",
         views.emp_dd_req,
         name="DD requests")
]
