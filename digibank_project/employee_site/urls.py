from django.urls import path
from django.urls.conf import include
from . import views

app_name = "employee_site"
urlpatterns = [
    path('',views.empHome,name='empHome'),
    path('login/',views.empLogin,name='empLogin'),
    path('logout/',views.empLogout,name='empLogout'),
    path('forgot/',views.forgotpass,name='forgot'),
    path('reset/',views.reset,name='reset'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    path('resetauth/',views.resetauth,name='resetauth'),
    path('auth/',views.auth,name='auth'),
    path("account_activation/",
         views.emp_account_act,
         name="Account Activation"),
    path("account_activation/<int:pk>/",
         views.emp_account_act,
         name="Account Activation"),
    path("dd_req/",
         views.emp_dd_req,
         name="DD Requests"),
    path("dd_req/<int:pk>/",
         views.emp_dd_req,
         name="DD Requests"),
    path("check_req/",
         views.emp_checks,
         name="Check Requests"),
    path("check_req/<int:pk>/",
         views.emp_checks,
         name="Check Requests")
]
