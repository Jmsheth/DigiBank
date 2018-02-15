from . import views
from django.urls import path

app_name = "login"

urlpatterns = [
    path('', views.home, name='cusHome'),
    path('login/', views.login, name='login'),
    path('auth/', views.auth, name='auth'),
    path('forgot/', views.forget, name='forgot'),
    path('reset/', views.reset, name='reset'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('resetauth/', views.resetauth, name='resetauth'),
    path('changepass/', views.changepass, name='changePass'),
    path('authreset/', views.resetpassauth, name='passauth'),
    path('logout/', views.logout, name='logout'),
    path('logout/', views.logout, name='logout'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('updateauth/',views.updateauth, name='updateauth'),
    path('userAccountSummary/', views.userAccountSummary, name='userAccountSummary'),
    path('authsummary/', views.authdetails, name='viewdetails'),
    path('userTransactionReport/', views.userTransactionReport, name='userTransactionReport'),
    path('authtxnreport/', views.authReportdetails, name='viewreport'),
    path('userFundsTransfer/', views.userFundsTransfer_vw.as_view(), name='userFundsTransfer'),
    # URLS for Changes included by <kashif>
    path('userAccountSummary', views.userAccountSummary, name='userAccountSummary'),
    path("request_checks/",
         views.user_check_req,
         name="Check Request"),
    path("dd_req/",
         views.user_dd_req,
         name="DD Request")
]