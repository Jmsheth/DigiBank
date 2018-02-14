from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.i18n import urlpatterns
from . import views
from django.urls import path

app_name = "login"

urlpatterns = [
    path('', views.home, name= 'cusHome'),
    path('login/', views.login, name='login'),
    path('auth/', views.auth, name='auth'),
    path('forgot/', views.forget,name='forgot'),
    path('reset/', views.reset, name='reset'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('resetauth/', views.resetauth, name='resetauth'),
    path('changepass/', views.changepass, name='changePass'),
    path('authreset/',views.resetpassauth,name='passauth'),
    path('logout/',views.logout,name='logout'),
    # URLS for Changes included by <kashif>
    path('userAccountSummary/',views.userAccountSummary_vw.as_view(),name='userAccountSummary'),
    path('userTransactionReport/',views.userTransactionReport_vw.as_view(), name='userTransactionReport'),
    path('userFundsTransfer/', views.userFundsTransfer_vw.as_view(), name='userFundsTransfer'),


]