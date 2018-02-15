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
    path('userTransactionReport/', views.userTransactionReport_vw.as_view(), name='userTransactionReport'),
    path('userFundsTransfer/', views.userFundsTransfer_vw.as_view(), name='userFundsTransfer'),
]